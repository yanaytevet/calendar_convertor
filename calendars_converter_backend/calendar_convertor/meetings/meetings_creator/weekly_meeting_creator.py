import re
from typing import List, Tuple, Dict, Optional

import fitz
from dateutil.parser import parse

from calendar_convertor.common.pdf_string_utils import PdfStringUtils
from calendar_convertor.common.time_utils import TimeUtils
from calendar_convertor.common.type_hints import JSONType, TimeType
from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.fitz_meeting_creator import FitzMeetingCreator


class WeeklyMeetingCreator(FitzMeetingCreator):
    DATA_REGEX = re.compile("(\S+) (\d+) (?:ןושאר|ינש|ישילש|יעיבר|ישימח|ישיש|תבש)")
    MEETING_REGEX = re.compile("(\d{2}):(\d{2}) - (\d{2}):(\d{2})(.*)")

    def create_meetings_from_page(self, pdf_page: fitz.Page) -> List[Meeting]:
        blocks = pdf_page.get_text('blocks')
        month_to_year = self.get_month_to_year(blocks)

        meetings = []
        last_date = None
        for block in blocks:
            text = block[4]
            new_date = self.get_date(text, month_to_year)
            if new_date is not None:
                last_date = new_date
                continue
            if last_date is None:
                continue
            meeting = self.get_meeting(text, last_date)
            if meeting is not None:
                meetings.append(meeting)
        return meetings

    def get_month_to_year(self, blocks: List[Tuple[str, ...]]) -> Dict[str, int]:
        months_arr = blocks[6][4].split("\n")
        months_arr = months_arr[:2]
        res = {}
        for month_text in months_arr:
            month_text = month_text.split(" - ")[-1]
            for word, new_word in self.MONTHS_MAP.items():
                month_text = month_text.replace(word, new_word)
            year, month, _ = month_text.split(" ")
            res[month] = int(year)
        return res

    def get_errors(self) -> List[JSONType]:
        return []

    def get_date(self, text: str, month_to_year: Dict[str, int]) -> Optional[TimeType]:
        match = self.DATA_REGEX.search(text)
        if match:
            month_hebrew = match.group(1)
            day = match.group(2)
            month = self.MONTHS_MAP[month_hebrew]
            return TimeUtils.make_aware(parse(f"{day} {month} {month_to_year[month]}", dayfirst=True))
        return None

    def get_meeting(self, text: str, last_date: TimeType) -> Optional[Meeting]:
        match = self.MEETING_REGEX.search(text)
        if match:
            end_hour = int(match.group(1))
            end_minutes = int(match.group(2))
            start_hour = int(match.group(3))
            start_minutes = int(match.group(4))
            meeting_text = PdfStringUtils.fix_text(match.group(5))
            meeting = Meeting(
                start_time=TimeUtils.combine_date_and_hour(last_date, start_hour, start_minutes),
                end_time=TimeUtils.combine_date_and_hour(last_date, end_hour, end_minutes),
                text=meeting_text,
                location="",
            )
            self.fix_meeting_time(meeting)
            return meeting
        return None
