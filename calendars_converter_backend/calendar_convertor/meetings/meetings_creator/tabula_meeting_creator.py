from abc import ABC, abstractmethod
from typing import List

import tabula
from pandas import DataFrame
from werkzeug.datastructures import FileStorage

from calendar_convertor.meetings.meeting import Meeting
from calendar_convertor.meetings.meetings_creator.meeting_creator import MeetingCreator


class TabulaMeetingCreator(MeetingCreator, ABC):

    def __init__(self, pdf_file: FileStorage):
        super().__init__(pdf_file)
        self.dfs: List[DataFrame] = tabula.read_pdf(pdf_file, pages='all', pandas_options={"header": None})

    def close(self) -> None:
        pass

    def get_meetings(self) -> List[Meeting]:
        res = []
        self.init()
        for _, df in enumerate(self.dfs):
            meetings = self.create_meetings_from_df(df)
            res.extend(meetings)
        return res

    def init(self):
        pass

    @abstractmethod
    def create_meetings_from_df(self, df: DataFrame) -> List[Meeting]:
        raise NotImplementedError()
