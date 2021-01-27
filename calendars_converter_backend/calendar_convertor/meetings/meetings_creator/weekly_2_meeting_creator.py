from typing import List

import fitz

from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.meeting_creator import MeetingCreator


class Weekly2MeetingCreator(MeetingCreator):
    def create_meetings_from_page(self, pdf_page: fitz.Page) -> List[Meeting]:
        return []
