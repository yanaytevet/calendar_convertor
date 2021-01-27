import io
from typing import List, BinaryIO

import xlsxwriter

from calendar_convertor.meetings.meeting import Meeting


class XlsCreator:
    TIME_FORMAT = "%Y-%m-%d %H:%M"

    def __init__(self):
        pass

    def create_file(self, meetings: List[Meeting]) -> BinaryIO:
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, 'start_time')
        worksheet.write(0, 1, 'end_time')
        worksheet.write(0, 2, 'text')
        worksheet.write(0, 3, 'location')
        worksheet.set_column(0, 1, 25)
        worksheet.set_column(2, 3, 100)

        index = 1

        for meeting in meetings:
            worksheet.write(index, 0, meeting.start_time.strftime(self.TIME_FORMAT))
            worksheet.write(index, 1, meeting.end_time.strftime(self.TIME_FORMAT))
            worksheet.write(index, 2, meeting.text)
            worksheet.write(index, 3, meeting.location)
            lines_count = meeting.text.count("\n")
            if lines_count > 0:
                worksheet.set_row(index, lines_count * 20 + 10)
            index += 1

        workbook.close()
        output.seek(0)
        print(output)
        return output
