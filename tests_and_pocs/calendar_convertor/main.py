import xlsxwriter

from calendar_convertor.convertor import Convertor


TIME_FORMAT = "%Y-%m-%d %H:%M"

if __name__ == '__main__':
    with open('calendar.csv', 'w', newline='') as csvfile:
        workbook = xlsxwriter.Workbook()
        worksheet = workbook.add_worksheet()
        worksheet.remove_timezone = True

        worksheet.write(0, 0, 'start_time')
        worksheet.write(0, 1, 'end_time')
        worksheet.write(0, 2, 'text')
        worksheet.set_column(0, 1, 25)
        worksheet.set_column(2, 2, 100)

        index = 1

        for meetings in Convertor().run_on_file("data/cal_2.pdf"):
            for meeting in meetings:
                worksheet.write(index, 0, meeting.start_time.strftime(TIME_FORMAT))
                worksheet.write(index, 1, meeting.end_time.strftime(TIME_FORMAT))
                worksheet.write(index, 2, meeting.text)
                lines_count = meeting.text.count("\n")
                if lines_count > 0:
                    worksheet.set_row(index, lines_count * 20 + 10)
                index += 1

        workbook.filename = 'calendar.xlsx'
        workbook.close()
