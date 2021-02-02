import os
from abc import ABC, abstractmethod
from abc import ABC, abstractmethod
from typing import List

from werkzeug.datastructures import FileStorage

from calendar_convertor.common.time_utils import TimeUtils
from calendar_convertor.common.type_hints import JSONType
from calendar_convertor.meetings.meeting import Meeting


class MeetingCreator(ABC):

    def __init__(self, pdf_file: FileStorage):
        self.pdf_file = pdf_file

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_meetings(self) -> List[Meeting]:
        raise NotImplementedError()

    @abstractmethod
    def get_errors(self) -> List[JSONType]:
        raise NotImplementedError()

    def get_file_name(self) -> str:
        base_name, ext = os.path.splitext(self.pdf_file.filename)
        return f"{base_name}.xlsx"

    @classmethod
    def fix_meeting_time(cls, meeting: Meeting) -> None:
        if meeting.end_time:
            while meeting.end_time < meeting.start_time:
                meeting.end_time = TimeUtils.add_days_to_date(meeting.end_time, 1)