import re
from typing import List, Pattern, Tuple

import fitz
from werkzeug.datastructures import FileStorage

from calendar_convertor.common.pdf_string_utils import PdfStringUtils
from calendar_convertor.common.time_utils import TimeUtils
from calendar_convertor.common.type_hints import JSONType
from calendar_convertor.elements.date_element import DateElement
from calendar_convertor.elements.element import Element
from calendar_convertor.elements.elements_collection import ElementsCollection
from calendar_convertor.elements.hour_element import HourElement
from calendar_convertor.elements.text_element import TextElement
from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meeting_time_calculator import MeetingTimeCalculator
from calendar_convertor.meetings.meetings_creator.fitz_meeting_creator import FitzMeetingCreator


class DailyMeetingCreator(FitzMeetingCreator):
    WANTED_HOURS = ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
    MAX_HOUR_IND = 12

    def __init__(self, pdf_file: FileStorage):
        super().__init__(pdf_file)
        self.regex_obj: Pattern = re.compile("\d+ \S+ \d+")

    def create_meetings_from_page(self, pdf_page: fitz.Page) -> List[Meeting]:
        hour_elements, upper_text_elements, lower_text_elements = self.get_time_and_text_elements(pdf_page)
        collections = ElementsCollection(
            upper_text_elements=upper_text_elements,
            lower_text_elements=lower_text_elements,
            meeting_elements=self.get_meeting_elements(pdf_page),
            hour_elements=hour_elements,
            date_elements=self.get_date_elements(pdf_page),
        )
        return self.create_meetings_from_elements_collection(collections)

    def create_meetings_from_elements_collection(self, raw_elements: ElementsCollection) -> List[Meeting]:
        meeting_time_calc = MeetingTimeCalculator.from_elements(raw_elements.date_elements, raw_elements.hour_elements)
        meeting_element_to_meeting = {}
        meeting_to_upper_text_elements = {}
        meeting_to_lower_text_elements = {}

        for meeting_element in raw_elements.meeting_elements:
            start_time, end_time = meeting_time_calc.get_datetimes(meeting_element)
            meeting = Meeting(text="", start_time=start_time, end_time=end_time, location="")
            meeting_element_to_meeting[meeting_element] = meeting
            meeting_to_upper_text_elements[meeting] = []
            meeting_to_lower_text_elements[meeting] = []

        meetings = raw_elements.meeting_elements[:]
        meetings.sort(key=lambda meeting_element: meeting_element.top, reverse=True)

        for text_element in raw_elements.upper_text_elements:
            for meeting_element in meetings:
                if meeting_element.contains(text_element, buffer=10):
                    meeting = meeting_element_to_meeting[meeting_element]
                    meeting_to_upper_text_elements[meeting].append(text_element)
                    break
        for text_element in raw_elements.lower_text_elements:
            for meeting_element in meetings:
                if meeting_element.contains(text_element, buffer=10):
                    meeting = meeting_element_to_meeting[meeting_element]
                    meeting_to_lower_text_elements[meeting].append(text_element)
                    break

        res = []
        for meeting, text_elements in meeting_to_upper_text_elements.items():
            text = "; ".join(text_element.text for text_element in text_elements)
            meeting.text = text
            if text:
                res.append(meeting)
        for meeting, text_elements in meeting_to_lower_text_elements.items():
            text = "; ".join(text_element.text for text_element in text_elements)
            meeting.location = text

        return res

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
        fill = drawing["fill"]
        if len(fill) != 3:
            return False
        r, g, b = fill
        if r == g and g == b:
            return False
        if drawing["rect"][2] - drawing["rect"][0] <= 10:
            return False
        return True

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

    def get_time_and_text_elements(self, pdf_page: fitz.Page) -> Tuple[List[HourElement], List[TextElement], List[TextElement]]:
        upper_texts_elements = []
        lower_texts_elements = []
        hours_elements = []
        current_hour_ind = 0
        for text_block in pdf_page.get_text('dict')["blocks"]:
            if "lines" not in text_block:
                continue
            lines = text_block["lines"]
            for line in lines:
                spans = line["spans"]
                for span in spans:
                    upper = self.is_bold(span)
                    text = span["text"].strip()
                    bbox = span["bbox"]
                    if text == "00":
                        continue
                    if current_hour_ind == self.MAX_HOUR_IND:
                        text = PdfStringUtils.fix_text(text)
                        text_element = TextElement(
                            top=bbox[1],
                            left=bbox[0],
                            bottom=bbox[3],
                            right=bbox[2],
                            text=text,
                        )
                        if upper:
                            upper_texts_elements.append(text_element)
                        else:
                            lower_texts_elements.append(text_element)
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
        return hours_elements, upper_texts_elements, lower_texts_elements

    def is_bold(self, span: JSONType) -> bool:
        return bool(span["flags"] & 2 ** 4)

    def get_errors(self) -> List[JSONType]:
        return []
