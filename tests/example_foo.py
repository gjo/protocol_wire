from typing import Protocol

from protocol_wire import Container, Registry


class Foo(Protocol):
    some: str


class FooImpl(Foo):
    some = "some"


def includeme(registry: Registry) -> None:
    def factory(container: Container) -> Foo:
        return FooImpl()

    registry.register_factory(factory, Foo)
