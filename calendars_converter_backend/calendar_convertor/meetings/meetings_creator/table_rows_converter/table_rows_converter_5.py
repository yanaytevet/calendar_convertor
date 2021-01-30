import re
from typing import List, Tuple, Optional

from calendar_convertor.common.pdf_string_utils import PdfStringUtils
from calendar_convertor.common.time_utils import TimeUtils
from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.table_rows_converter.table_rows_converter import TableRowsConverter


class TableRowsConverter5(TableRowsConverter):
    DATE_REGEX = re.compile("\d{2}/\d{2}/\d{4}")

    def __init__(self):
        super().__init__()
        self.time_format = "%d/%m/%Y %H:%M:%S"
        self.remove_empty = True

    def create_meetings(self, blocks: List[Tuple[str, ...]], page_number: int):
        if page_number == 0 or self.ignore_first_line:
            blocks = blocks[1:]
        meetings = []
        for block in blocks:
            line_text = block[4]
            line_arr = self.break_line_to_arr(line_text)
            date_index = self.get_date_index(line_arr)
            if date_index is None:
                continue
            text = self.extract_text_from_arr_and_indexes(line_arr, 1, date_index)
            location = self.extract_text_from_arr_and_indexes(line_arr, date_index + 3, None)
            date_str = line_arr[date_index]
            start_hour_str = line_arr[date_index + 1]
            end_hour_str = line_arr[date_index + 2]
            meeting = Meeting(
                text=text,
                location=location,
                start_time=TimeUtils.date_from_str_format(f"{date_str} {start_hour_str}", self.time_format),
                end_time=TimeUtils.date_from_str_format(f"{date_str} {end_hour_str}", self.time_format),
            )
            self.fix_meeting_end(meeting)
            meetings.append(meeting)
        return meetings

    def get_date_index(self, line_arr: List[str]) -> Optional[int]:
        for index, value in enumerate(line_arr):
            if self.DATE_REGEX.match(value):
                return index
        return None

