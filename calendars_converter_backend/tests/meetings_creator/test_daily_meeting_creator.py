from werkzeug.datastructures import FileStorage

from calendar_convertor.common.time_utils import TimeUtils
from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.daily_meeting_creator import DailyMeetingCreator
from calendar_convertor.meetings.meetings_creator.meeting_creator import MeetingCreator
from tests.meetings_creator.base_test_meeting_creator import BaseTestMeetingCreator


class TestDailyMeetingCreator(BaseTestMeetingCreator):

    @classmethod
    def get_creator(cls, file_obj: FileStorage) -> MeetingCreator:
        return DailyMeetingCreator(file_obj)

    def test_daily_1(self):
        meetings = self.get_meetings("daily/daily_1")
        self.assert_meetings([
            Meeting(text="אבי חליבה - ס 'נ.ש.מ",
                    location="אצל שאול; שאול מרידור",
                    start_time=TimeUtils.create_aware_datetime(2019, 1, 2, 8, 30),
                    end_time=TimeUtils.create_aware_datetime(2019, 1, 2, 9, 15)),
            Meeting(text="יוגב + לוריא",
                    location="אצל שאול ; שאול מרידור",
                    start_time=TimeUtils.create_aware_datetime(2019, 1, 2, 9, 30),
                    end_time=TimeUtils.create_aware_datetime(2019, 1, 2, 10, 0)),
            Meeting(text="פגישת היכרות עם שי-לי שפיגלמן -ישראל דיגיטלית",
                    location="אצל שאול ,משרד האוצר קפלן 1 קומה 2 חדר226; שאול מרידור",
                    start_time=TimeUtils.create_aware_datetime(2019, 1, 2, 11, 30),
                    end_time=TimeUtils.create_aware_datetime(2019, 1, 2, 12, 30)),
            Meeting(text="עופר שוטפים",
                    location="אצל שאול ; שאול מרידור",
                    start_time=TimeUtils.create_aware_datetime(2019, 1, 2, 13, 30),
                    end_time=TimeUtils.create_aware_datetime(2019, 1, 2, 14, 0)),
            Meeting(text="חברת חשמל -עופר בלוך",
                    location="אצל סגן השר ;יצחק כהן",
                    start_time=TimeUtils.create_aware_datetime(2019, 1, 2, 13, 45),
                    end_time=TimeUtils.create_aware_datetime(2019, 1, 2, 14, 15)),
            Meeting(text="סולקנים :סגן השר,; שאול מרידור ,ינקי",
                    location="אצל סגן שר האוצר יצחק כ; יצחק כהן",
                    start_time=TimeUtils.create_aware_datetime(2019, 1, 2, 14, 0),
                    end_time=TimeUtils.create_aware_datetime(2019, 1, 2, 15, 0)),
            Meeting(text="ישיבת הנהלה",
                    location="אצל שאול ;שאול מרידור",
                    start_time=TimeUtils.create_aware_datetime(2019, 1, 2, 15, 0),
                    end_time=TimeUtils.create_aware_datetime(2019, 1, 2, 15, 30)),
            Meeting(text="הכנה לרוביק",
                    location="אצל שאול ; שאול מרידור",
                    start_time=TimeUtils.create_aware_datetime(2019, 1, 2, 15, 45),
                    end_time=TimeUtils.create_aware_datetime(2019, 1, 2, 16, 15)),
            Meeting(text="נסיעות שיתופיות",
                    location="אצל שאול; שאול מרידור",
                    start_time=TimeUtils.create_aware_datetime(2019, 1, 2, 16, 0),
                    end_time=TimeUtils.create_aware_datetime(2019, 1, 2, 17, 0)),
            Meeting(text="עם ר 'עירית באר-שבע",
                    location="אצל שאול; שאול מרידור",
                    start_time=TimeUtils.create_aware_datetime(2019, 1, 2, 17, 0),
                    end_time=TimeUtils.create_aware_datetime(2019, 1, 2, 18, 0)),
        ], meetings)

    def test_daily_4(self):
        meetings = self.get_meetings("daily/daily_4")
        self.assert_meetings([], meetings)

    def test_daily_5(self):
        meetings = self.get_meetings("daily/daily_5")
        self.assert_meetings([
            Meeting(text="סיור עם צוות חינוך",
                    location="""ליבורנו 17 בת ים ,בי"ס הנשיא שמורה לךחנייה מול בית הספר ברחבת בית הכנסת; )לכשתגיע למקום ליצור קשר עם מיטל( 052-3604065; שאול מרידור""",
                    start_time=TimeUtils.create_aware_datetime(2019, 1, 10, 8, 30),
                    end_time=TimeUtils.create_aware_datetime(2019, 1, 10, 14, 30)),
        ], meetings)

    def test_daily_6(self):
        meetings = self.get_meetings("daily/daily_6")
        self.assert_meetings([
            Meeting(text="ישיבת צוותים - 2050  הישיבה תתקיים בזום",
                    location="""ל .מנכ"ל; אודי אדירי""",
                    start_time=TimeUtils.create_aware_datetime(2020, 4, 1, 9, 30),
                    end_time=TimeUtils.create_aware_datetime(2020, 4, 1, 10, 30),
                    ),
            Meeting(text="""שיחת זום פתוחה לכלל עובדי המשרד - עם מנכ"ל המשרד""",
                    location="אודי אדירי",
                    start_time=TimeUtils.create_aware_datetime(2020, 4, 1, 11, 0),
                    end_time=TimeUtils.create_aware_datetime(2020, 4, 1, 12, 0),
                    ),
            Meeting(text="הנהלה - הישיבה תתקיים בזום",
                    location="אודי אדירי",
                    start_time=TimeUtils.create_aware_datetime(2020, 4, 1, 13, 00),
                    end_time=TimeUtils.create_aware_datetime(2020, 4, 1, 14, 30),
                    ),
        ], meetings)

    def test_daily_8(self):
        meetings = self.get_meetings("daily/daily_8")
        self.assert_meetings(meetings, [])
