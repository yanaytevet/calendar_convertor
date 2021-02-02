from abc import ABC, abstractmethod
from typing import List

import fitz
from werkzeug.datastructures import FileStorage

from calendar_convertor.elements.elements_collection import ElementsCollection
from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meeting_time_calculator import MeetingTimeCalculator
from calendar_convertor.meetings.meetings_creator.meeting_creator import MeetingCreator


class FitzMeetingCreator(MeetingCreator, ABC):

    def __init__(self, pdf_file: FileStorage):
        super().__init__(pdf_file)
        self.pdf_document: fitz.Document = fitz.Document(stream=self.pdf_file.read(), filetype="pdf")

    def close(self) -> None:
        self.pdf_document.close()

    def get_meetings(self) -> List[Meeting]:
        res = []
        self.init()
        for pdf_page in self.pdf_document:
            meetings = self.create_meetings_from_page(pdf_page)
            res.extend(meetings)
        return res

    def init(self):
        pass

    @abstractmethod
    def create_meetings_from_page(self, pdf_page: fitz.Page) -> List[Meeting]:
        raise NotImplementedError()

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
