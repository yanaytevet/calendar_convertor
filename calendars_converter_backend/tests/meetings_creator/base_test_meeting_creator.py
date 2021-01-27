
import unittest
from abc import abstractmethod
from typing import List

from werkzeug.datastructures import FileStorage

from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.meeting_creator import MeetingCreator


class BaseTestMeetingCreator(unittest.TestCase):
    PRINT = False

    def assert_file(self, file_name: str, wanted_meetings: List[Meeting]) -> None:
        with open(f"data/{file_name}.pdf", "rb") as f:
            file_obj = FileStorage(f, filename=file_name)
            meetings = self.get_creator(file_obj).get_meetings()
            meetings.sort(key=lambda meeting: (meeting.start_time, meeting.text))
            wanted_meetings.sort(key=lambda meeting: (meeting.start_time, meeting.text))
            for wanted_meeting, meeting in zip(wanted_meetings, meetings):
                if self.PRINT:
                    print(wanted_meeting)
                    print(meeting)
                self.assertEqual(wanted_meeting, meeting)
            self.assertEqual(len(wanted_meetings), len(meetings))

    @classmethod
    @abstractmethod
    def get_creator(cls, file_obj: FileStorage) -> MeetingCreator:
        raise NotImplementedError()
