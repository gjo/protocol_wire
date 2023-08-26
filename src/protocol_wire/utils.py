from typing import Any, Protocol


def is_protocol(t: Any) -> bool:
    return getattr(t, "_is_protocol", False)


def is_delivered_protocol(t: Any) -> bool:
    return t is not Protocol and is_protocol(t)
