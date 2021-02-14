from werkzeug.datastructures import FileStorage

from calendar_convertor.common.time_utils import TimeUtils
from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.meeting_creator import MeetingCreator
from calendar_convertor.meetings.meetings_creator.weekly_meeting_creator import WeeklyMeetingCreator
from tests.meetings_creator.base_test_meeting_creator import BaseTestMeetingCreator


class TestWeeklyMeetingCreator(BaseTestMeetingCreator):

    @classmethod
    def get_creator(cls, file_obj: FileStorage) -> MeetingCreator:
        return WeeklyMeetingCreator(file_obj)

    def test_weekly_1(self):
        meetings = self.get_meetings("weekly/weekly_1")
        meetings.sort(key=lambda meeting: (meeting.start_time, meeting.text))
        self.assert_meetings_len(meetings, 1393)
        self.print_meetings(meetings, 24)
        self.assert_meetings_indexes(
            [
                (0, Meeting(text="- חדוה בר (לשכה ירושלים) סימה",
                            location="לשכה ירושלים",
                            start_time=TimeUtils.create_aware_datetime(2018, 12, 30, 8, 0),
                            end_time=TimeUtils.create_aware_datetime(2018, 12, 30, 8, 30))),
                (1, Meeting(text='''- חדוה (חדר ישיבות קומה -4 קרייה)  שב"א ומס"ב''',
                            location="חדר ישיבות קומה -4 קרייה",
                            start_time=TimeUtils.create_aware_datetime(2018, 12, 30, 8, 30),
                            end_time=TimeUtils.create_aware_datetime(2018, 12, 30, 9, 30))),
                (13, Meeting(text="סימה -עדכון פורום סגנים בנושא המלצה למתן",
                            location="",
                            start_time=TimeUtils.create_aware_datetime(2018, 12, 30, 16, 0),
                            end_time=TimeUtils.create_aware_datetime(2018, 12, 30, 16, 30))),
                (14, Meeting(text="אוצר החייל",
                            location="",
                            start_time=TimeUtils.create_aware_datetime(2018, 12, 31, 7, 30),
                            end_time=TimeUtils.create_aware_datetime(2018, 12, 31, 8, 0))),
                (18, Meeting(text="ועידת תחזיות של כלכליסט - מפקחת בשעה",
                            location="",
                            start_time=TimeUtils.create_aware_datetime(2018, 12, 31, 11, 0),
                            end_time=TimeUtils.create_aware_datetime(2018, 12, 31, 13, 0))),
            ],
            meetings
        )

    def test_weekly_2(self):
        meetings = self.get_meetings("weekly/weekly_2")
        meetings.sort(key=lambda meeting: (meeting.start_time, meeting.text))
        self.print_meetings(meetings, 0)
        self.assert_meetings_len(meetings, 592)
        self.assert_meetings_indexes(
            [
                (0, Meeting(text="""- מנכ"ל משרד (טלפונית) מלי פינקלשטיין - שוטף""",
                            location="טלפונית",
                            start_time=TimeUtils.create_aware_datetime(2020, 6, 28, 9, 0),
                            end_time=TimeUtils.create_aware_datetime(2020, 6, 28, 9, 30))),
            ],
            meetings
        )

    def test_weekly_3(self):
        meetings = self.get_meetings("weekly/weekly_3")
        meetings.sort(key=lambda meeting: (meeting.start_time, meeting.text))
        self.print_meetings(meetings, 0)
        self.assert_meetings_len(meetings, 895)
        self.assert_meetings_indexes(
            [
                (0, Meeting(text="""- מתן ( אצל שירה) שוטף מתן +שירה גרינברג""",
                            location=" אצל שירה",
                            start_time=TimeUtils.create_aware_datetime(2018, 12, 30, 11,),
                            end_time=TimeUtils.create_aware_datetime(2018, 12, 30, 12))),
            ],
            meetings
        )
