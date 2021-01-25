import datetime
from dataclasses import dataclass

from calendar_convertor.elements_creators.elements.element import Element


@dataclass
class HourElement(Element):
    hour: int
