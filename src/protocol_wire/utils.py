from typing import Any, Protocol


def is_protocol(t: Any) -> bool:  # noqa: ANN401
    return getattr(t, "_is_protocol", False)


def is_delivered_protocol(t: Any) -> bool:  # noqa: ANN401
    return t is not Protocol and is_protocol(t)


# ANN401: Dynamically typed expressions (typing.Any) are disallowed in `X`
