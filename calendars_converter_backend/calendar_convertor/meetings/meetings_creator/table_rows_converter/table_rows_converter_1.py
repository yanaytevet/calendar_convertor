from calendar_convertor.meetings.meetings_creator.table_rows_converter.table_rows_converter import TableRowsConverter


class TableRowsConverter1(TableRowsConverter):

    def __init__(self):
        super().__init__()
        self.text_indexes = [(0, -6)]
        self.start_time_indexes = [(-5, -3)]
        self.end_time_indexes = [(-2, None)]
        self.time_format = "%d/%m/%Y %H:%M"
        self.remove_empty = True
        self.texts_to_remove = {"םוי"}


