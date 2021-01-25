from abc import ABC, abstractmethod

import fitz

from calendar_convertor.elements_creators.elements.elements_collection import ElementsCollection


class ElementsCreator(ABC):
    @abstractmethod
    def run(self, pdf_file: fitz.Page) -> ElementsCollection:
        raise NotImplementedError()
