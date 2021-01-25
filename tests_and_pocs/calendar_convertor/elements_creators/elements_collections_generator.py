from typing import Iterator, Dict, Type

import fitz

from calendar_convertor.calendar_type import CalendarType
from calendar_convertor.elements_creators.elements.elements_collection import ElementsCollection
from calendar_convertor.elements_creators.elements_creator import ElementsCreator
from calendar_convertor.elements_creators.vector_pdf_daily_elements_creator import VectorPdfDailyElementsCreator


class ElementsCollectionsGenerator:
    CALENDAR_TYPE_TO_ELEMENTS_CREATOR: Dict[CalendarType, Type[ElementsCreator]] = {
        CalendarType.VECTOR_PDF_DAILY: VectorPdfDailyElementsCreator
    }

    def generate(self, pdf_file: fitz.Document, calendar_type: CalendarType) -> Iterator[ElementsCollection]:
        elements_creator = self.CALENDAR_TYPE_TO_ELEMENTS_CREATOR[calendar_type]()
        for page in pdf_file:
            yield elements_creator.run(page)
