from abc import ABC, abstractmethod

import fitz

from calendar_convertor.elements_creators.elements.elements_collection import ElementsCollection


class ElementsCreator(ABC):
    @abstractmethod
    def run(self, pdf_file: fitz.Page) -> ElementsCollection:
        raise NotImplementedError()

    @classmethod
    def is_ascii(cls, letter):
        return ord(letter) < 128

    @classmethod
    def fix_text(cls, text: str) -> str:
        arr = []
        ascii_arr = []
        for letter in text:
            if not cls.is_ascii(letter):
                if ascii_arr:
                    ascii_arr.reverse()
                    arr.extend(ascii_arr)
                    ascii_arr = []
                arr.append(letter)
            else:
                ascii_arr.append(letter)
        if ascii_arr:
            ascii_arr.reverse()
            arr.extend(ascii_arr)
        return "".join(arr)[::-1].strip()
