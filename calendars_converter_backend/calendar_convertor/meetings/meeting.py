from dataclasses import dataclass

from calendar_convertor.common.type_hints import TimeType


@dataclass(unsafe_hash=True)
class Meeting:
    text: str
    location: str
    start_time: TimeType
    end_time: TimeType
