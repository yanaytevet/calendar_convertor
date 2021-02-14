from werkzeug.datastructures import FileStorage

from calendar_convertor.common.time_utils import TimeUtils
from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.meeting_creator import MeetingCreator
from calendar_convertor.meetings.meetings_creator.table_meeting_creator import TableMeetingCreator
from tests.meetings_creator.base_test_meeting_creator import BaseTestMeetingCreator


class TestTableMeetingCreator(BaseTestMeetingCreator):
    @classmethod
    def get_creator(cls, file_obj: FileStorage) -> MeetingCreator:
        return TableMeetingCreator(file_obj)

    def test_table_1(self):
        meetings = self.get_meetings("table/table_1")
        self.print_meetings(meetings, 0)
        self.assert_meetings_len(meetings, 139)
        self.assert_meetings_indexes(
            [
                (0, Meeting(text="תקשורת",
                            location="",
                            start_time=TimeUtils.create_aware_datetime(2020, 8, 2, 9),
                            end_time=None)),
                (1, Meeting(text="ישבת שרינו כחול-לבן",
                            location="",
                            start_time=TimeUtils.create_aware_datetime(2020, 8, 2, 9, 30),
                            end_time=None)),
                (20, Meeting(text="מליאה",
                             location="",
                             start_time=TimeUtils.create_aware_datetime(2020, 8, 5, 11),
                             end_time=None)),
                (51, Meeting(text='פ.ע מנכ"לית',
                             location="",
                             start_time=TimeUtils.create_aware_datetime(2020, 8, 12, 15, 30),
                             end_time=None)),
                (100, Meeting(text="תקשורת",
                              location="",
                              start_time=TimeUtils.create_aware_datetime(2020, 8, 23, 18),
                              end_time=None)),
            ],
            meetings
        )

    def test_table_3(self):
        meetings = self.get_meetings("table/table_3")
        self.assert_meetings_len(meetings, 139)
        # self.print_meetings(meetings, 0)
        self.assert_meetings_indexes(
            [
                (0, Meeting(text="תקשורת",
                            location="",
                            start_time=TimeUtils.create_aware_datetime(2020, 8, 2, 9),
                            end_time=None)),
                (1, Meeting(text="ישבת שרינו כחול-לבן",
                            location="",
                            start_time=TimeUtils.create_aware_datetime(2020, 8, 2, 9, 30),
                            end_time=None)),
                (20, Meeting(text="מליאה",
                             location="",
                             start_time=TimeUtils.create_aware_datetime(2020, 8, 5, 11),
                             end_time=None)),
                (51, Meeting(text='פ.ע מנכ"לית',
                             location="",
                             start_time=TimeUtils.create_aware_datetime(2020, 8, 12, 15, 30),
                             end_time=None)),
                (100, Meeting(text="תקשורת",
                              location="",
                              start_time=TimeUtils.create_aware_datetime(2020, 8, 23, 18),
                              end_time=None)),
            ],
            meetings
        )

    def test_table_4(self):
        meetings = self.get_meetings("table/table_4")
        self.assert_meetings_len(meetings, 93)
        self.assert_meetings_indexes(
            [
                (0, Meeting(text="‫השבעת‬ ‫הממשלה‬",
                            location="כנסת",
                            start_time=TimeUtils.create_aware_datetime(2020, 5, 17, 13, 30),
                            end_time=TimeUtils.create_aware_datetime(2020, 5, 17, 21, 30))),
                (2, Meeting(text="טקס חילופי שרות - המשרד לשיוויון חברתי",
                            location="‫ירושלים‬",
                            start_time=TimeUtils.create_aware_datetime(2020, 5, 18, 14, 0),
                            end_time=TimeUtils.create_aware_datetime(2020, 5, 18, 15, 30))),
                (28, Meeting(text="פגישת היכרות עם ארגוני הסביבה",
                             location="‫ירושלים‬",
                             start_time=TimeUtils.create_aware_datetime(2020, 6, 1, 12, 0),
                             end_time=TimeUtils.create_aware_datetime(2020, 6, 1, 14, 30))),
                (29, Meeting(text="‫כנסת‬",
                             location="‫ירושלים‬",
                             start_time=TimeUtils.create_aware_datetime(2020, 6, 1, 15, 0),
                             end_time=TimeUtils.create_aware_datetime(2020, 6, 2, 3, 1))),
            ],
            meetings
        )

    def test_table_5(self):
        meetings = self.get_meetings("table/table_5")
        self.assert_meetings_len(meetings, 828)
        self.assert_meetings_indexes(
            [
                (0, Meeting(text="פורום מטה",
                            location='משרדו של המנכ"ל',
                            start_time=TimeUtils.create_aware_datetime(2019, 6, 2, 12, 0),
                            end_time=TimeUtils.create_aware_datetime(2019, 6, 2, 13, 10))),
                (1, Meeting(text='נסיעת השר לארה"ב יוני 2019',
                            location='משרדו של המנכ"ל',
                            start_time=TimeUtils.create_aware_datetime(2019, 6, 2, 13, 10),
                            end_time=TimeUtils.create_aware_datetime(2019, 6, 2, 13, 30))),
                (20, Meeting(text='פ"ע - ראש תחום בכיר',
                             location='אצל מנכ"ל',
                             start_time=TimeUtils.create_aware_datetime(2019, 6, 10, 14, 0),
                             end_time=TimeUtils.create_aware_datetime(2019, 6, 10, 16, 30))),
                (39, Meeting(text='עבודה על מצגת ונאום GC4I',
                             location='משרדו של המנכ"ל',
                             start_time=TimeUtils.create_aware_datetime(2019, 6, 16, 16, 30),
                             end_time=TimeUtils.create_aware_datetime(2019, 6, 16, 17, 0))),
                (40, Meeting(text='מנכ"ל במילואים - יום שלם',
                             location='',
                             start_time=TimeUtils.create_aware_datetime(2019, 6, 17),
                             end_time=TimeUtils.create_aware_datetime(2019, 6, 17))),
            ],
            meetings
        )

    def test_table_6(self):
        meetings = self.get_meetings("table/table_6")
        self.assert_meetings_len(meetings, 200)
        self.assert_meetings_indexes(
            [
                (0, Meeting(
                    text="שלום דסקל     תוכנית להגדלת התעסוקה בהייטק  2,להקמת מרכזי מצוינות 0 אלף\rמשרות על פני 5 שנים",
                    location='לשכת שר י-ם',
                    start_time=TimeUtils.create_aware_datetime(2020, 6, 1, 12, 0),
                    end_time=TimeUtils.create_aware_datetime(2020, 6, 1, 12, 30))),
                (1, Meeting(text='פ.היכרות-איילת זלדין',
                            location='ל.מנכ"ל י-ם',
                            start_time=TimeUtils.create_aware_datetime(2020, 6, 1, 13, 0),
                            end_time=TimeUtils.create_aware_datetime(2020, 6, 1, 13, 30))),
                (28, Meeting(text='נסיעה לקרייה בתל אביב',
                             location='',
                             start_time=TimeUtils.create_aware_datetime(2020, 6, 4, 13, 0),
                             end_time=TimeUtils.create_aware_datetime(2020, 6, 4, 13, 30))),
                (50, Meeting(text="הפורום הכלכלי -מס ,2' יום ב׳ 8 ביוני 2020",
                             location='בני ברק',
                             start_time=TimeUtils.create_aware_datetime(2020, 6, 8, 18),
                             end_time=TimeUtils.create_aware_datetime(2020, 6, 8, 19, 30))),
            ],
            meetings
        )

    def test_table_8(self):
        meetings = self.get_meetings("table/table_8")

    def test_table_9(self):
        meetings = self.get_meetings("table/table_9")
        self.assert_meetings_len(meetings, 317)
        self.assert_meetings_indexes(
            [
                (0, Meeting(text="ראש מועצת עמנואל – אליהו גפני",
                            location='',
                            start_time=TimeUtils.create_aware_datetime(2020, 1, 1, 9, 0),
                            end_time=TimeUtils.create_aware_datetime(2020, 1, 1, 10, 0))),
                (1, Meeting(text="שי חג'ג (ראש מועצת מרחבים)",
                            location='',
                            start_time=TimeUtils.create_aware_datetime(2020, 1, 1, 10, 30),
                            end_time=TimeUtils.create_aware_datetime(2020, 1, 1, 11, 0))),
                (28, Meeting(text='ישיבת ממשלה',
                             location='',
                             start_time=TimeUtils.create_aware_datetime(2020, 1, 12, 10, 30),
                             end_time=TimeUtils.create_aware_datetime(2020, 1, 12, 11, 30))),
                (50, Meeting(text="שלומי מגנזי סגן ראש מועצה מטה יהודה  18:00-",
                             location='',
                             start_time=TimeUtils.create_aware_datetime(2020, 1, 15, 18),
                             end_time=TimeUtils.create_aware_datetime(2020, 1, 15, 18, 30))),
            ],
            meetings
        )
