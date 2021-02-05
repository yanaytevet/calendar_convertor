
import unittest
from abc import abstractmethod
from typing import List, Tuple

from werkzeug.datastructures import FileStorage

from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.meeting_creator import MeetingCreator


class BaseTestMeetingCreator(unittest.TestCase):
    def get_meetings(self, file_name: str) -> List[Meeting]:
        with open(f"data/{file_name}.pdf", "rb") as f:
            file_obj = FileStorage(f, filename=file_name)
            creator = self.get_creator(file_obj)
            meetings = creator.get_meetings()
            errors = creator.get_errors()
            if errors:
                print("Errors:")
                for error in errors:
                    print(error)
        meetings.sort(key=lambda meeting: (meeting.start_time, meeting.text))
        return meetings

    def print_meetings(self, meetings: List[Meeting], index: int) -> None:
        print(meetings[index])

    def assert_meetings(self, wanted_meetings: List[Meeting], actual_meetings: List[Meeting]) -> None:
        wanted_meetings.sort(key=lambda meeting: (meeting.start_time, meeting.text))
        actual_meetings.sort(key=lambda meeting: (meeting.start_time, meeting.text))
        for wanted_meeting, meeting in zip(wanted_meetings, actual_meetings):
            self.assertEqual(wanted_meeting, meeting)

    def assert_meetings_len(self, actual_meetings: List[Meeting], meeting_amount: int) -> None:
        self.assertEqual(meeting_amount, len(actual_meetings))

    def assert_meetings_indexes(self, wanted_meetings_indexes: List[Tuple[int, Meeting]], actual_meetings: List[Meeting]) -> None:
        for index, meeting in wanted_meetings_indexes:
            actual_meeting = actual_meetings[index]
            self.assertEqual(self.fix_text(meeting.text), actual_meeting.text, msg=f"text at index {index}")
            self.assertEqual(self.fix_text(meeting.location), actual_meeting.location, msg=f"location at index {index}")
            self.assertEqual(meeting.start_time, actual_meeting.start_time, msg=f"start_time at index {index}")
            self.assertEqual(meeting.end_time, actual_meeting.end_time, msg=f"end_time at index {index}")

    @classmethod
    def fix_text(cls, text: str) -> str:
        return text.replace("\u202c", "").replace("\u202b", "")

    @classmethod
    @abstractmethod
    def get_creator(cls, file_obj: FileStorage) -> MeetingCreator:
        raise NotImplementedError()
