import datetime
import typing as t

_JSONType_0 = t.Union[str, int, float, bool, None, t.Dict[str, t.Any], t.List[t.Any]]
_JSONType_1 = t.Union[str, int, float, bool, None, t.Dict[str, _JSONType_0], t.List[_JSONType_0]]
_JSONType_2 = t.Union[str, int, float, bool, None, t.Dict[str, _JSONType_1], t.List[_JSONType_1]]
_JSONType_3 = t.Union[str, int, float, bool, None, t.Dict[str, _JSONType_2], t.List[_JSONType_2]]
JSONType = t.Union[str, int, float, bool, None, t.Dict[str, _JSONType_3], t.List[_JSONType_3]]

DateType = datetime.date
TimeType = datetime.datetime
TimeDeltaType = datetime.timedelta
