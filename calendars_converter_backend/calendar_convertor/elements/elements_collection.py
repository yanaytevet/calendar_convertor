from dataclasses import dataclass
from typing import List

from calendar_convertor.elements.date_element import DateElement
from calendar_convertor.elements.element import Element
from calendar_convertor.elements.hour_element import HourElement
from calendar_convertor.elements.text_element import TextElement


@dataclass
class ElementsCollection:
    upper_text_elements: List[TextElement]
    lower_text_elements: List[TextElement]
    meeting_elements: List[Element]
    hour_elements: List[HourElement]
    date_elements: List[DateElement]
