from typing import Protocol

import pytest


class PlainClass:
    ...


class DeliveredProtocol(Protocol):
    ...


class NestedProtocol(DeliveredProtocol, Protocol):
    ...


class OtherProtocol(Protocol):
    ...


class DiamondProtocol(NestedProtocol, OtherProtocol, Protocol):
    ...


class Implementation(DiamondProtocol):
    ...


@pytest.mark.parametrize(
    "type_,expected",
    [
        (int, False),
        (str, False),
        (object, False),
        (PlainClass, False),
        (Protocol, True),
        (DeliveredProtocol, True),
        (NestedProtocol, True),
        (DiamondProtocol, True),
        (Implementation, False),
    ],
)
def test_is_protocol(type_: type, expected: bool) -> None:
    from protocol_wire.utils import is_protocol

    assert is_protocol(type_) is expected


@pytest.mark.parametrize(
    "type_,expected",
    [
        (int, False),
        (str, False),
        (object, False),
        (PlainClass, False),
        (Protocol, False),
        (DeliveredProtocol, True),
        (NestedProtocol, True),
        (DiamondProtocol, True),
        (Implementation, False),
    ],
)
def test_is_delivered_protocol(type_: type, expected: bool) -> None:
    from protocol_wire.utils import is_delivered_protocol

    assert is_delivered_protocol(type_) is expected
