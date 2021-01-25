from dataclasses import dataclass

from calendar_convertor.elements_creators.elements.element import Element
from common.type_hints import DateType


@dataclass
class DateElement(Element):
    date: DateType
