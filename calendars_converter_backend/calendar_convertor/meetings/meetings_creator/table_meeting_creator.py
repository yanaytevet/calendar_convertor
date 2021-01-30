from typing import List, Tuple, Optional

import fitz
from werkzeug.datastructures import FileStorage

from calendar_convertor.common.pdf_string_utils import PdfStringUtils
from calendar_convertor.common.time_utils import TimeUtils
from calendar_convertor.common.type_hints import TimeType
from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.meeting_creator import MeetingCreator
from calendar_convertor.meetings.meetings_creator.table_rows_converter.table_rows_converter import TableRowsConverter
from calendar_convertor.meetings.meetings_creator.table_rows_converter.table_rows_converter_1 import TableRowsConverter1
from calendar_convertor.meetings.meetings_creator.table_rows_converter.table_rows_converter_3 import TableRowsConverter3
from calendar_convertor.meetings.meetings_creator.table_rows_converter.table_rows_converter_4 import TableRowsConverter4
from calendar_convertor.meetings.meetings_creator.table_rows_converter.table_rows_converter_5 import TableRowsConverter5


class TableMeetingCreator(MeetingCreator):
    FIRST_LINE_1 = '''אשונ
םוקימ
הלחתה
ףוס
'''
    FIRST_LINE_3 = """הלחתה ךיראת
 
הלחתה תעש
 
אשונ
 
"""
    FIRST_LINE_4 = """ךיראת
 הלחתה תעש
 םויס תעש
אשונ
 םוקימ
"""
    FIRST_LINE_5 = '''דסמ
אשונ
הלחתה ךיראת
הלחתה תעש
םויס תעש
םוקימ
'''

    def __init__(self, pdf_file: FileStorage):
        super().__init__(pdf_file)
        self.table_rows_converter: Optional[TableRowsConverter] = None

    def create_meetings_from_page(self, pdf_page: fitz.Page) -> List[Meeting]:
        blocks = pdf_page.get_text("blocks", flags=fitz.TEXT_PRESERVE_SPANS)
        if pdf_page.number == 0:
            first_line_text = blocks[0][4]
            self.set_converter_from_first_line(first_line_text)

        return self.table_rows_converter.create_meetings(blocks, page_number=pdf_page.number)

    def set_converter_from_first_line(self, first_line_text: str) -> None:
        # print(f"first_line_text '{first_line_text}'")
        if first_line_text == self.FIRST_LINE_1:
            self.table_rows_converter = TableRowsConverter1()
        elif first_line_text == self.FIRST_LINE_3:
            self.table_rows_converter = TableRowsConverter3()
        elif first_line_text == self.FIRST_LINE_4:
            self.table_rows_converter = TableRowsConverter4()
        elif first_line_text == self.FIRST_LINE_5:
            self.table_rows_converter = TableRowsConverter5()
        else:
            raise Exception("Unknown Format")
