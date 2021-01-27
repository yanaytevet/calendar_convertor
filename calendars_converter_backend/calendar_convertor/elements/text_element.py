from dataclasses import dataclass

from calendar_convertor.elements.element import Element


@dataclass
class TextElement(Element):
    text: str
