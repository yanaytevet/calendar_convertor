from dataclasses import dataclass

from common.type_hints import TimeType


@dataclass(unsafe_hash=True)
class Meeting:
    text: str
    start_time: TimeType
    end_time: TimeType
