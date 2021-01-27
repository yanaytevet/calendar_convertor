from dataclasses import dataclass

from calendar_convertor.elements.element import Element


@dataclass
class HourElement(Element):
    hour: int
