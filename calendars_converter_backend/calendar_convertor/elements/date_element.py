from dataclasses import dataclass

from calendar_convertor.common.type_hints import DateType
from calendar_convertor.elements.element import Element


@dataclass
class DateElement(Element):
    date: DateType
