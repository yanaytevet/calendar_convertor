from typing import Tuple, List

from calendar_convertor.common.pdf_string_utils import PdfStringUtils
from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.table_rows_converter.table_rows_converter import TableRowsConverter


class TableRowsConverter3(TableRowsConverter):

    def __init__(self):
        super().__init__()
        self.text_indexes = [(3, None)]
        self.start_time_indexes = [(0, 3)]
        self.time_format = "%d/%m/%Y %H:%M"
        self.remove_empty = False
        self.min_size_or_append = 7

    def create_meetings(self, blocks: List[Tuple[str, ...]], page_number: int):
        if page_number == 0 or self.ignore_first_line:
            blocks = blocks[1:]
        meetings = []
        last_meeting = None
        for block in blocks:
            line_text = block[4]
            line_arr = self.break_line_to_arr(line_text)
            if self.min_size_or_append is not None and len(line_arr) < self.min_size_or_append:
                if last_meeting:
                    new_text = self.extract_append_text_from_arr(line_arr)
                    last_meeting.text = f"{last_meeting.text} {new_text}".strip()
                continue
            text = self.extract_text_from_arr(line_arr)
            last_meeting = Meeting(
                text=text,
                location="",
                start_time=self.extract_start_time_from_arr(line_arr),
                end_time=self.extract_end_time_from_arr(line_arr),
            )
            meetings.append(last_meeting)
        return meetings

    def extract_append_text_from_arr(self, line_arr: List[str]) -> str:
        line_text = " ".join(PdfStringUtils.fix_text(text) for text in line_arr)
        line_text = line_text.replace(' " ', '"').replace(" '", "'")
        return line_text
