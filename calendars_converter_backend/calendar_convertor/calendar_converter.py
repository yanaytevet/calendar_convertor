from typing import BinaryIO, Tuple, Dict, Type

from werkzeug.datastructures import FileStorage

from calendar_convertor.calendar_type import CalendarType
from calendar_convertor.meetings.meetings_creator.meeting_creator import MeetingCreator
from calendar_convertor.meetings.meetings_creator.daily_meeting_creator import DailyMeetingCreator
from calendar_convertor.meetings.meetings_creator.table_meeting_creator import TableMeetingCreator
from calendar_convertor.meetings.meetings_creator.weekly_1_meeting_creator import Weekly1MeetingCreator
from calendar_convertor.meetings.meetings_creator.weekly_2_meeting_creator import Weekly2MeetingCreator
from calendar_convertor.xls_creator import XlsCreator


class CalendarConverter:
    CALENDAR_TYPE_TO_MEETING_CREATOR_CLS: Dict[CalendarType, Type[MeetingCreator]] = {
        CalendarType.DAILY: DailyMeetingCreator,
        CalendarType.WEEKLY_1: Weekly1MeetingCreator,
        CalendarType.WEEKLY_2: Weekly2MeetingCreator,
        CalendarType.TABLE: TableMeetingCreator,
    }

    def __init__(self, pdf_file: FileStorage, calendar_type: CalendarType):
        self.pdf_file = pdf_file
        self.calendar_type = calendar_type

    def convert_to_xls(self) -> Tuple[BinaryIO, str]:
        creator = self.CALENDAR_TYPE_TO_MEETING_CREATOR_CLS[self.calendar_type](self.pdf_file)
        meetings = creator.get_meetings()
        erros = creator.get_errors()
        creator.close()
        return XlsCreator().create_file(meetings, erros), creator.get_file_name()
