import calendar
from datetime import datetime, timedelta
from typing import Optional

import pytz
from tzlocal import get_localzone

from .type_hints import TimeType, TimeDeltaType, DateType


class TimeUtils:
    LOCAL_TZ = get_localzone()
    DEFAULT_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
    SIMPLE_FORMAT = "%Y-%m-%d"

    @classmethod
    def now(cls) -> TimeType:
        # noinspection PyUnresolvedReferences
        return cls.LOCAL_TZ.localize(datetime.now())

    @classmethod
    def create_aware_datetime(cls, *args, **kwargs) -> TimeType:
        date_obj = datetime(*args, **kwargs)
        return cls.make_aware(date_obj)

    @classmethod
    def zero_time(cls) -> TimeType:
        date_obj = datetime(1970, 1, 1)
        return cls.make_aware(datetime_obj=date_obj, timezone='utc')

    @classmethod
    def inf_time(cls) -> TimeType:
        date_obj = datetime(3000, 1, 1)
        return cls.make_aware(datetime_obj=date_obj, timezone='utc')

    @classmethod
    def to_simple_str(cls, datetime_obj: TimeType) -> Optional[str]:
        return cls.to_format_str(datetime_obj=datetime_obj, date_format=cls.SIMPLE_FORMAT)

    @classmethod
    def to_format_str(cls, datetime_obj: TimeType, date_format: str) -> Optional[str]:
        if datetime_obj is None or date_format is None:
            return None
        return datetime_obj.strftime(date_format)

    @classmethod
    def from_simple_str(cls, datetime_str: str) -> Optional[TimeType]:
        return cls.from_format_str(datetime_str, cls.SIMPLE_FORMAT)

    @classmethod
    def from_format_str(cls, datetime_str: str, date_format: str, timezone: Optional[str] = None) -> Optional[TimeType]:
        if datetime_str is None:
            return None
        return cls.make_aware(datetime.strptime(datetime_str, date_format), timezone=timezone)

    @classmethod
    def to_default_str(cls, datetime_obj: TimeType) -> Optional[str]:
        if datetime_obj is None:
            return None
        return datetime_obj.strftime(cls.DEFAULT_FORMAT)

    @classmethod
    def from_default_str(cls, datetime_str: str) -> Optional[TimeType]:
        return cls.from_format_str(datetime_str, cls.DEFAULT_FORMAT)

    @classmethod
    def create_to_default_str(cls, *args, **kwargs) -> Optional[str]:
        return cls.to_default_str(cls.create_aware_datetime(*args, **kwargs))

    @classmethod
    def aware_to_default_str(cls, datetime_obj: TimeType) -> Optional[str]:
        if datetime_obj is None:
            return None
        return cls.to_default_str(datetime_obj)

    @classmethod
    def make_aware(cls, datetime_obj: TimeType, timezone: Optional[str] = None) -> TimeType:
        if timezone:
            timezone_obj = pytz.timezone("UTC")
        else:
            timezone_obj = cls.LOCAL_TZ
        return timezone_obj.localize(datetime_obj)

    @classmethod
    def aware_seconds_since_epoch(cls, aware_datetime_obj: TimeType) -> float:
        return (aware_datetime_obj - cls.zero_time()).total_seconds()

    @classmethod
    def aware_date_from_seconds_since_epoch(cls, total_seconds: float) -> TimeType:
        return cls.make_aware(datetime.utcfromtimestamp(total_seconds))

    @classmethod
    def add_years_to_date(cls, date_obj: TimeType, years: int) -> TimeType:
        new_year = date_obj.year + years
        last_day = calendar.monthrange(new_year, date_obj.month)[1]
        return cls.create_aware_datetime(date_obj.year + years, date_obj.month, min(date_obj.day, last_day))

    @classmethod
    def add_months_to_date(cls, date_obj: TimeType, months: int) -> TimeType:
        total_months = date_obj.month + months - 1
        add_years = total_months // 12
        new_months = total_months % 12 + 1
        new_year = date_obj.year + add_years
        last_day = calendar.monthrange(new_year, new_months)[1]
        day = min(date_obj.day, last_day)
        return cls.create_aware_datetime(new_year, new_months, day)

    @classmethod
    def add_days_to_date(cls, date_obj: TimeType, days: int) -> TimeType:
        return date_obj + timedelta(days=days)

    @classmethod
    def is_less_equal_than_x_months_apart(cls, date_obj_1: TimeType, date_obj_2: TimeType, months: int) -> bool:
        new_date_1 = cls.add_months_to_date(date_obj_1, months)
        return new_date_1 >= date_obj_2

    @classmethod
    def get_months_between(cls, date_obj_2: TimeType, date_obj_1: TimeType, includes_same_day: bool = True) -> int:
        years_diff = date_obj_2.year - date_obj_1.year
        months_diff = date_obj_2.month - date_obj_1.month + 12 * years_diff
        if includes_same_day:
            if date_obj_2.day < date_obj_1.day:
                months_diff -= 1
        else:
            if date_obj_2.day <= date_obj_1.day:
                months_diff -= 1
        return months_diff

    @classmethod
    def date_from_str_format(cls, datetime_str: str, date_format: str) -> TimeType:
        return cls.make_aware(datetime.strptime(datetime_str, date_format))

    @classmethod
    def remove_hours_from_date(cls, date_obj: TimeType) -> TimeType:
        return date_obj.replace(hour=0, minute=0, second=0, microsecond=0)

    @classmethod
    def get_month_end_date_aware(cls, date_obj: TimeType) -> TimeType:
        year = date_obj.year
        month = date_obj.month
        return cls.get_last_day_in_month_date_aware(year=year, month=month)

    @classmethod
    def get_last_day_in_month_date_aware(cls, year: int, month: int) -> TimeType:
        last_day = calendar.monthrange(year, month)[1]
        return cls.create_aware_datetime(year, month, last_day)

    @classmethod
    def get_first_day_in_month_date_aware(cls, year: int, month: int) -> TimeType:
        return cls.create_aware_datetime(year, month, 1)

    @classmethod
    def get_first_day_in_month_date_aware_from_date_obj(cls, date_obj: TimeType) -> TimeType:
        return cls.get_first_day_in_month_date_aware(year=date_obj.year, month=date_obj.month)

    @classmethod
    def timedelta_to_seconds(cls, time_delta: timedelta) -> float:
        return time_delta.total_seconds()

    @classmethod
    def timedelta_to_days(cls, time_delta: timedelta) -> float:
        time_delta_sec = cls.timedelta_to_seconds(time_delta=time_delta)
        return time_delta_sec / (24 * 60 * 60)

    @classmethod
    def timedelta_from_days(cls, days: float) -> TimeDeltaType:
        return timedelta(seconds=days * 24 * 60 * 60)

    @classmethod
    def combine_date_and_hour(cls, date: DateType, hour: float, minutes: float = 0) -> TimeType:
        return cls.create_aware_datetime(date.year, date.month, date.day) + timedelta(hours=hour, minutes=minutes)
