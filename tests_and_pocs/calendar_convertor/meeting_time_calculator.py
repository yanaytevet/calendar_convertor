from typing import List, Tuple, Optional

from common.time_utils import TimeUtils
from common.type_hints import DateType, TimeType
from elements_creators.elements.date_element import DateElement
from elements_creators.elements.element import Element
from elements_creators.elements.hour_element import HourElement


class MeetingTimeCalculator:

    def __init__(self, a: float, b: float, date_limits: List[Tuple[float, float, DateType]]):
        self.a = a
        self.b = b
        self.date_limits = date_limits

    def get_datetimes(self, element: Element) -> Tuple[Optional[TimeType], Optional[TimeType]]:
        date = self.get_date_from_element(element)
        if date is None:
            return None, None
        top = element.top
        bottom = element.bottom
        start_hour = self.get_hour_float(top)
        end_hour = self.get_hour_float(bottom)
        start_time = TimeUtils.combine_date_and_hour(date, start_hour)
        end_time = TimeUtils.combine_date_and_hour(date, end_hour)
        return start_time, end_time

    def get_date_from_element(self, element: Element) -> Optional[DateType]:
        for left, right, date in self.date_limits:
            if element.left >= left and element.right <= right:
                return date
        return None

    def get_hour_float(self, location: float) -> float:
        hour = location * self.a + self.b
        return round(hour * 4) / 4

    @classmethod
    def from_elements(cls, date_elements: List[DateElement], hour_elements: List[HourElement]) -> "MeetingTimeCalculator":
        hour_element = hour_elements[0]
        next_hour_element = hour_elements[1]
        a, b = cls.get_a_b(hour_element, next_hour_element)
        date_limits = [(date_element.left, date_element.right, date_element.date) for date_element in date_elements]
        return MeetingTimeCalculator(a, b, date_limits)

    @classmethod
    def get_a_b(cls, hour_element: HourElement, next_hour_element: HourElement) -> Tuple[float, float]:
        t = hour_element.top
        b = next_hour_element.top
        h = hour_element.hour
        b_line = h - (t/(b-t))
        a_line = 1 / (b-t)
        return a_line, b_line
