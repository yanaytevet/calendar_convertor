from abc import ABC, abstractmethod
from typing import List

import fitz
from werkzeug.datastructures import FileStorage

from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.meeting_creator import MeetingCreator


class FitzMeetingCreator(MeetingCreator, ABC):
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
