import typing as t

# Service 接收的数据
ServiceData = t.TypeVar("ServiceData", bound=t.Dict[str, t.Any])
