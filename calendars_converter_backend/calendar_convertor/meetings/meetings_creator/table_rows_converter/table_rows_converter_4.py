from typing import Tuple, List

from calendar_convertor.common.pdf_string_utils import PdfStringUtils
from calendar_convertor.common.time_utils import TimeUtils
from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.table_rows_converter.table_rows_converter import TableRowsConverter


class TableRowsConverter4(TableRowsConverter):

    def __init__(self):
        super().__init__()
        self.text_indexes = [(3, None)]
        self.start_time_indexes = [(0, 2)]
        self.end_time_indexes = [(0, 1), (2, 3)]
        self.time_format = "%d.%m.%y %H:%M"
        self.remove_empty = True
        self.last_date_str = None

    def create_meetings(self, blocks: List[Tuple[str, ...]], page_number: int):
        if page_number == 0 or self.ignore_first_line:
            blocks = blocks[1:]
        meetings = []
        for block in blocks:
            line_text = block[4]
            line_arr = self.break_line_to_arr(line_text)
            if not line_arr:
                continue
            if self.is_date(line_arr[0]):
                date_str = line_arr[0]
                self.last_date_str = date_str
                start_hour_str = line_arr[1]
                end_hour_str = line_arr[2]
                start_text_index = 3
            else:
                start_hour_str = line_arr[0]
                end_hour_str = line_arr[1]
                start_text_index = 2
                date_str = self.last_date_str
            text = self.extract_text_from_arr_and_indexes(line_arr, start_text_index, -1)
            meeting = Meeting(
                text=text,
                location=PdfStringUtils.fix_text(line_arr[-1]),
                start_time=TimeUtils.date_from_str_format(f"{date_str} {start_hour_str}", self.time_format),
                end_time=TimeUtils.date_from_str_format(f"{date_str} {end_hour_str}", self.time_format),
            )
            self.fix_meeting_end(meeting)
            meetings.append(meeting)
        return meetings

    def is_date(self, date_str) -> bool:
        return date_str.count(".") == 2
