from calendar_convertor.convertor import Convertor
import csv

if __name__ == '__main__':
    with open('calendar.csv', 'w', newline='') as csvfile:
        fieldnames = ['start_time', 'end_time', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for meetings in Convertor().run_on_file("data/cal_2.pdf"):
            for meeting in meetings:
                writer.writerow({'start_time': meeting.start_time, 'end_time': meeting.end_time, 'text': meeting.text})
