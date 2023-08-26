from typing import TYPE_CHECKING, Protocol

import pytest

if TYPE_CHECKING:
    from protocol_wire.registry import Container


class Foo(Protocol):
    some: str


class FooImpl(Foo):
    some = "some"

    @classmethod
    def factory(cls, container: "Container") -> "Foo":
        return cls()


def foo_factory(container: "Container") -> Foo:
    return FooImpl()


async def async_foo_factory(container: "Container") -> Foo:
    return FooImpl()


def test_factory() -> None:
    from protocol_wire.registry import Registry

    registry = Registry()
    registry.register_factory(foo_factory, Foo)
    fac = registry.find_factory(Foo)
    assert fac is foo_factory

    container = registry.create_container()
    ins = container.find(Foo)
    assert isinstance(ins, FooImpl)

    ins2 = container.find(Foo)
    assert isinstance(ins2, FooImpl)
    assert ins is ins2


def test_factory_named() -> None:
    from protocol_wire.registry import Registry

    registry = Registry()
    registry.register_factory(foo_factory, Foo, name="name")
    fac = registry.find_factory(Foo, name="name")
    assert fac is foo_factory

    container = registry.create_container()
    ins = container.find(Foo, name="name")
    assert isinstance(ins, FooImpl)


@pytest.mark.asyncio
async def test_factory_async() -> None:
    from protocol_wire.registry import Registry

    registry = Registry()
    registry.register_factory(async_foo_factory, Foo)
    fac = registry.find_factory(Foo)
    assert fac is async_foo_factory

    container = registry.create_container()
    ins = await container.async_find(Foo)
    assert isinstance(ins, FooImpl)

    ins2 = await container.async_find(Foo)
    assert isinstance(ins2, FooImpl)
    assert ins is ins2


@pytest.mark.asyncio
async def test_factory_await_no_async() -> None:
    from protocol_wire.registry import Registry

    registry = Registry()
    registry.register_factory(foo_factory, Foo)
    fac = registry.find_factory(Foo)
    assert fac is foo_factory

    container = registry.create_container()
    ins = await container.async_find(Foo)
    assert isinstance(ins, FooImpl)


def test_factory_method() -> None:
    from protocol_wire.registry import Registry

    registry = Registry()
    registry.register_factory(FooImpl.factory, Foo)
    fac = registry.find_factory(Foo)
    assert fac == FooImpl.factory  # FIXME: actual is bounded

    container = registry.create_container()
    ins = container.find(Foo)
    assert isinstance(ins, FooImpl)


def test_instance() -> None:
    from protocol_wire.registry import Registry, Singleton

    registry = Registry()
    foo = FooImpl()
    registry.register_instance(foo, Foo)
    fac = registry.find_factory(Foo)
    assert isinstance(fac, Singleton)
    assert fac.instance is foo
    ins = registry.find_instance(Foo)
    assert ins is foo

    container = registry.create_container()
    ins2 = container.find(Foo)
    assert isinstance(ins2, FooImpl)


def test_raises_already_registered() -> None:
    from protocol_wire.exceptions import AlreadyRegistered
    from protocol_wire.registry import Registry

    registry = Registry()
    registry.register_factory(foo_factory, Foo)
    with pytest.raises(AlreadyRegistered):
        registry.register_factory(foo_factory, Foo)


def test_raises_does_not_registered() -> None:
    from protocol_wire.exceptions import DoesNotRegistered
    from protocol_wire.registry import Registry

    registry = Registry()
    with pytest.raises(DoesNotRegistered):
        registry.find_factory(Foo)


def test_raises_is_not_singleton() -> None:
    from protocol_wire.exceptions import IsNotSingleton
    from protocol_wire.registry import Registry

    registry = Registry()
    registry.register_factory(foo_factory, Foo)
    with pytest.raises(IsNotSingleton):
        registry.find_instance(Foo)


def test_raises_does_not_support_awaitable() -> None:
    from protocol_wire.exceptions import DoesNotSupportAwaitable
    from protocol_wire.registry import Registry

    registry = Registry()
    registry.register_factory(async_foo_factory, Foo)
    fac = registry.find_factory(Foo)
    assert fac is async_foo_factory

    container = registry.create_container()
    with pytest.raises(DoesNotSupportAwaitable):
        container.find(Foo)
