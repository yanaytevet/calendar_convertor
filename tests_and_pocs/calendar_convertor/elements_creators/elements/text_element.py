from dataclasses import dataclass

from calendar_convertor.elements_creators.elements.element import Element


@dataclass
class TextElement(Element):
    text: str
