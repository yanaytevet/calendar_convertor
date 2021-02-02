import re
from typing import List, Optional

import pandas as pd
from pandas import DataFrame, Series
from werkzeug.datastructures import FileStorage

from calendar_convertor.common.pdf_string_utils import PdfStringUtils
from calendar_convertor.common.time_utils import TimeUtils
from calendar_convertor.common.type_hints import TimeType, JSONType
from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.tabula_meeting_creator import TabulaMeetingCreator
from dateutil.parser import parse


class TableMeetingCreator(TabulaMeetingCreator):
    TEXT = "נושא"
    LOCATION = "מיקום"
    END_DATE = ["תאריך סיו", "תאריך סו"]
    START_DATE = ["תאריך התחלה", "תאריך"]
    START_HOUR = ["התחלה", "עת התחל"]
    END_HOUR = ["סוף", "סיום", "עת סו", "עת סיו"]
    STR_TO_REMOVE = ["zoom", "zoon", "ZOOM"]

    def __init__(self, pdf_file: FileStorage):
        super().__init__(pdf_file)
        self.text_index = None
        self.location_index = None
        self.start_date_index = None
        self.end_date_index = None
        self.start_hour_index = None
        self.end_hour_index = None
        self.last_date_str = ""
        self.error_rows = []

    def create_meetings_from_df(self, df: DataFrame) -> List[Meeting]:
        if self.should_set_column_indexes():
            self.set_column_indexes(df)

        meetings = []
        for _, row in df.iterrows():
            meeting = self.convert_row_to_meeting(row)
            if meeting:
                meetings.append(meeting)
        return meetings

    def should_set_column_indexes(self) -> None:
        return self.text_index is None

    def set_column_indexes(self, df: DataFrame) -> None:
        first_line = df.iloc[0]
        for column_index, value in first_line.iteritems():
            value = str(value)
            if value == self.TEXT:
                self.text_index = column_index
            elif value == self.LOCATION:
                self.location_index = column_index
            elif self.is_contained(value, self.END_DATE):
                self.end_date_index = column_index
            elif self.is_contained(value, self.START_DATE):
                self.start_date_index = column_index
            elif self.is_contained(value, self.START_HOUR):
                self.start_hour_index = column_index
            elif self.is_contained(value, self.END_HOUR):
                self.end_hour_index = column_index
        if self.end_date_index is None:
            self.end_date_index = self.start_date_index

    def is_contained(self, value: str, options: List[str]) -> bool:
        for option in options:
            if option in value:
                return True
        return False

    def is_row_headers(self, row: Series) -> bool:
        return row[self.text_index] == self.TEXT

    def convert_row_to_meeting(self, row: Series) -> Optional[Meeting]:
        try:
            if self.is_row_headers(row):
                return None
            text = row[self.text_index]
            location = self.get_location(row)

            start_time = self.get_start_time_from_row(row)
            end_time = self.get_end_time_from_row(row)
            if start_time is None:
                return None
            meeting = Meeting(
                text=text,
                location=location,
                start_time=start_time,
                end_time=end_time,
            )
            self.fix_meeting_time(meeting)
            return meeting
        except Exception:
            self.error_rows.append(row)

    def get_location(self, row: Series) -> str:
        location = row[self.location_index] if self.location_index is not None else ""
        if pd.isna(location):
            return ""
        return location

    def get_start_time_from_row(self, row: Series) -> Optional[TimeType]:
        if self.start_date_index is not None:
            date_str = row[self.start_date_index]
            if not pd.isna(date_str):
                self.last_date_str = date_str
            else:
                date_str = self.last_date_str
            time_str = f"{date_str} {row[self.start_hour_index]}"
        else:
            time_str = f"{row[self.start_hour_index]}"
        time_str = self.fix_time_str(time_str)
        return TimeUtils.make_aware(parse(time_str, dayfirst=True))

    def get_end_time_from_row(self, row: Series) -> Optional[TimeType]:
        if self.end_hour_index is None:
            return None
        if self.end_date_index is not None:
            date_str = row[self.end_date_index]
            if not pd.isna(date_str):
                self.last_date_str = date_str
            else:
                date_str = self.last_date_str
            time_str = f"{date_str} {row[self.end_hour_index]}"
        else:
            time_str = f"{row[self.end_hour_index]}"
        time_str = self.fix_time_str(time_str)
        return TimeUtils.make_aware(parse(time_str, dayfirst=True))

    def fix_time_str(self, time_str: str) -> str:
        time_str = PdfStringUtils.remove_non_ascii(time_str)
        for str_to_remove in self.STR_TO_REMOVE:
            time_str = time_str.split(str_to_remove)[0]
        time_str = re.sub(':(\d\d)(\d\d)/', r':\1 \2/', time_str)
        return time_str.strip()

    def get_errors(self) -> List[JSONType]:
        return [list(row.to_dict().values()) for row in self.error_rows]
