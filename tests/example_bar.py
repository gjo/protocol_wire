from typing import Protocol

from protocol_wire import Container, Registry


class Bar(Protocol):
    other: str


class BarImpl(Bar):
    other = "other"


def includeme(registry: Registry) -> None:
    def factory(container: Container) -> Bar:
        return BarImpl()

    registry.register_factory(factory, Bar)
