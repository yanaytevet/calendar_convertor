from abc import ABC, abstractmethod
from typing import Tuple, List, Optional

from calendar_convertor.common.pdf_string_utils import PdfStringUtils
from calendar_convertor.common.time_utils import TimeUtils
from calendar_convertor.common.type_hints import TimeType
from calendar_convertor.meetings.meeting import Meeting


class TableRowsConverter(ABC):
    def __init__(self):
        self.ignore_first_line = False
        self.text_indexes = None
        self.start_time_indexes = None
        self.end_time_indexes = None
        self.time_format = None
        self.remove_empty = False
        self.texts_to_remove = set()

    def create_meetings(self, blocks: List[Tuple[str, ...]], page_number: int):
        if page_number == 0 or self.ignore_first_line:
            blocks = blocks[1:]
        meetings = []
        for block in blocks:
            line_text = block[4]
            line_arr = self.break_line_to_arr(line_text)
            print(line_arr)
            text = self.extract_text_from_arr(line_arr)
            last_meeting = Meeting(
                text=text,
                location="",
                start_time=self.extract_start_time_from_arr(line_arr),
                end_time=self.extract_end_time_from_arr(line_arr),
            )
            meetings.append(last_meeting)
        return meetings

    def break_line_to_arr(self, line: str) -> List[str]:
        arr = [text.strip() for text in line.split("\n")]
        arr = [text for text in arr if (text not in self.texts_to_remove) and not (self.remove_empty and not text)]
        return arr

    def extract_text_from_arr(self, line_arr: List[str]) -> str:
        line_text = " ".join(PdfStringUtils.fix_text(text) for text in
                             self.line_arr_and_indexes_to_arr(line_arr, self.text_indexes))
        line_text = line_text.replace(' " ', '"').replace(" '", "'").strip()
        return line_text

    def extract_text_from_arr_and_indexes(self, line_arr: List[str], start_index: int, end_index: Optional[int]) -> str:
        line_text = " ".join(PdfStringUtils.fix_text(text) for text in line_arr[start_index: end_index])
        line_text = line_text.replace(' " ', '"').replace(" '", "'").strip()
        return line_text


    def extract_start_time_from_arr(self, line_arr: List[str]) -> TimeType:
        return self.line_arr_and_indexes_to_date(line_arr, self.start_time_indexes)

    def extract_end_time_from_arr(self, line_arr: List[str]) -> Optional[TimeType]:
        if self.end_time_indexes is None:
            return None
        return self.line_arr_and_indexes_to_date(line_arr, self.end_time_indexes)

    def line_arr_and_indexes_to_date(self, line_arr: List[str], indexes: List[Tuple[int, int]]):
        line_end_time = " ".join(self.line_arr_and_indexes_to_arr(line_arr, indexes))
        return TimeUtils.date_from_str_format(line_end_time, self.time_format)

    @classmethod
    def line_arr_and_indexes_to_arr(cls, line_arr: List[str], indexes: List[Tuple[int, int]]) -> List[str]:
        res = []
        for index_start, index_end in indexes:
            res.extend(line_arr[index_start: index_end])
        return res

    def fix_meeting_end(self, meeting: Meeting) -> None:
        if meeting.end_time is None:
            return
        while meeting.end_time < meeting.start_time:
            meeting.end_time = TimeUtils.add_days_to_date(meeting.end_time, 1)
