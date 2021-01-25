from dataclasses import dataclass
from typing import List

from calendar_convertor.elements_creators.elements.date_element import DateElement
from calendar_convertor.elements_creators.elements.element import Element
from calendar_convertor.elements_creators.elements.hour_element import HourElement
from calendar_convertor.elements_creators.elements.text_element import TextElement


@dataclass
class ElementsCollection:
    text_elements: List[TextElement]
    meeting_elements: List[Element]
    hour_elements: List[HourElement]
    date_elements: List[DateElement]
