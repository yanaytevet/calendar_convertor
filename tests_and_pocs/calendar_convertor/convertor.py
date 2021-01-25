from typing import Optional, List, Iterator

import fitz

from calendar_convertor.calendar_type import CalendarType
from calendar_convertor.elements_creators.elements.elements_collection import ElementsCollection
from calendar_convertor.elements_creators.elements_collections_generator import ElementsCollectionsGenerator
from calendar_convertor.meeting import Meeting
from meeting_time_calculator import MeetingTimeCalculator


class Convertor:
    def __init__(self):
        self.file_path: Optional[str] = None
        self.pdf_file: Optional[fitz.Document] = None

    def run_on_file(self, file_path: str) -> Iterator[List[Meeting]]:
        print(file_path)
        self.file_path = file_path
        self.pdf_file = fitz.open(self.file_path)
        calendar_type = self.get_calendar_type()
        for raw_elements in ElementsCollectionsGenerator().generate(self.pdf_file, calendar_type):
            yield self.create_meetings(raw_elements)

    def get_calendar_type(self) -> CalendarType:
        return CalendarType.VECTOR_PDF_DAILY

    def create_meetings(self, raw_elements: ElementsCollection) -> List[Meeting]:
        meeting_time_calc = MeetingTimeCalculator.from_elements(raw_elements.date_elements, raw_elements.hour_elements)
        meeting_element_to_meeting = {}
        meeting_to_text_elements = {}

        for meeting_element in raw_elements.meeting_elements:
            start_time, end_time = meeting_time_calc.get_datetimes(meeting_element)
            meeting = Meeting(text="", start_time=start_time, end_time=end_time)
            meeting_element_to_meeting[meeting_element] = meeting
            meeting_to_text_elements[meeting] = []

        meetings = raw_elements.meeting_elements[:]
        meetings.sort(key=lambda meeting_element: meeting_element.top, reverse=True)

        for text_element in raw_elements.text_elements:
            for meeting_element in meetings:
                if meeting_element.contains(text_element, buffer=10):
                    meeting = meeting_element_to_meeting[meeting_element]
                    meeting_to_text_elements[meeting].append(text_element)
                    break

        res = []
        for meeting, text_elements in meeting_to_text_elements.items():
            text = "\n".join(text_element.text for text_element in text_elements)
            meeting.text = text
            if text:
                res.append(meeting)

        return res
