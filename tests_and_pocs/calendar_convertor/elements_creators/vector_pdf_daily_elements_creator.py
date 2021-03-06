import re
from typing import List, Tuple
from typing.re import Pattern

import fitz

from calendar_convertor.elements_creators.elements.date_element import DateElement
from calendar_convertor.elements_creators.elements.element import Element
from calendar_convertor.elements_creators.elements.elements_collection import ElementsCollection
from calendar_convertor.elements_creators.elements.hour_element import HourElement
from calendar_convertor.elements_creators.elements.text_element import TextElement
from calendar_convertor.elements_creators.elements_creator import ElementsCreator
from common.time_utils import TimeUtils
from common.type_hints import JSONType


class VectorPdfDailyElementsCreator(ElementsCreator):
    MONTHS_MAP = {
        "ראוני": "Jan",
        "ראורבפ": "Feb",
        "ץרמ": "Mar",
        "לירפא": "Apr",
        "יאמ": "May",
        "ינוי": "Jun",
        "ילוי": "Jul",
        "טסוגוא": "Aug",
        "רבמטפס": "Sep",
        "רבוטקוא": "Oct",
        "רבמבונ": "Nov",
        "רבמצד": "Dec",
    }
    WANTED_HOURS = ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
    MAX_HOUR_IND = 12

    def __init__(self):
        self.regex_obj: Pattern = re.compile("\d+ \S+ \d+")

    def run(self, pdf_page: fitz.Page) -> ElementsCollection:
        hour_elements, text_elements = self.get_time_and_text_elements(pdf_page)
        return ElementsCollection(
            text_elements=text_elements,
            meeting_elements=self.get_meeting_elements(pdf_page),
            hour_elements=hour_elements,
            date_elements=self.get_date_elements(pdf_page),
        )

        # page.get_text('dict')
        # page.get_text_blocks()

    def get_meeting_elements(self, pdf_page: fitz.Page) -> List[Element]:
        res = []
        for drawing in pdf_page.getDrawings():
            if self.drawing_is_meeting(drawing):
                res.append(Element(
                    left=drawing["rect"][0],
                    top=drawing["rect"][1],
                    right=drawing["rect"][2],
                    bottom=drawing["rect"][3],
                ))
        return res

    @classmethod
    def drawing_is_meeting(cls, drawing: JSONType) -> bool:
        if not drawing["fill"]:
            return False
        r, g, b = drawing["fill"]
        if r == g and g == b:
            return False
        if drawing["rect"][2] - drawing["rect"][0] <= 10:
            return False
        return True

    def get_text_elements(self, pdf_page: fitz.Page) -> List[TextElement]:
        return []

    def get_date_elements(self, pdf_page: fitz.Page) -> List[DateElement]:
        for text_block in pdf_page.get_text('dict')["blocks"]:
            if "lines" not in text_block:
                continue
            lines = text_block["lines"]
            spans = lines[0]["spans"]
            if len(spans) != 2:
                continue
            text = spans[1]["text"]
            if not self.regex_obj.match(text):
                continue
            for word, new_word in self.MONTHS_MAP.items():
                text = text.replace(word, new_word)
            date_obj = TimeUtils.from_format_str(text, "%Y %b %d").date()
            return [
                DateElement(
                    top=0,
                    left=0,
                    bottom=pdf_page.CropBox[3],
                    right=pdf_page.CropBox[2],
                    date=date_obj,
                )
            ]
        return []

    def get_time_and_text_elements(self, pdf_page: fitz.Page) -> Tuple[List[HourElement], List[TextElement]]:
        texts_elements = []
        hours_elements = []
        current_hour_ind = 0
        for text_block in pdf_page.get_text('dict')["blocks"]:
            if "lines" not in text_block:
                continue
            lines = text_block["lines"]
            spans = lines[0]["spans"]
            for span in spans:
                text = span["text"]
                bbox = span["bbox"]
                if current_hour_ind == self.MAX_HOUR_IND:
                    text = self.fix_text(text)
                    texts_elements.append(TextElement(
                        top=bbox[1],
                        left=bbox[0],
                        bottom=bbox[3],
                        right=bbox[2],
                        text=text,
                    ))
                elif self.WANTED_HOURS[current_hour_ind] == text:
                    hours_elements.append(HourElement(
                        top=bbox[1],
                        left=bbox[0],
                        bottom=bbox[3],
                        right=bbox[2],
                        hour=int(text),
                    ))
                    current_hour_ind += 1
                else:
                    current_hour_ind = 0
                    hours_elements = []
        return hours_elements, texts_elements
