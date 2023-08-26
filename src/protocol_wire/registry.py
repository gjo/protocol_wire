import inspect
from typing import Any, Awaitable, Generic, Optional, Protocol, TypeVar, Union, cast

from .exceptions import AlreadyRegistered, DoesNotRegistered, DoesNotSupportAwaitable, IsNotSingleton
from .utils import is_delivered_protocol

T = TypeVar("T")
Tcov = TypeVar("Tcov", covariant=True)


class Factory(Protocol[Tcov]):
    def __call__(self, container: "Container") -> Union[Tcov, Awaitable[Tcov]]:
        ...


class Singleton(Generic[T]):
    def __init__(self, instance: T) -> None:
        self.instance: T = instance

    def __call__(self, contaner: "Container") -> T:
        return self.instance


class Registry:
    def __init__(self) -> None:
        self.adaptors: dict[tuple[Optional[type], str], Any] = {}

    def register_factory(self, factory: Factory[T], spec: Optional[type[T]] = None, *, name: str = "") -> None:
        assert spec is None or is_delivered_protocol(spec)
        k = spec, name
        if k in self.adaptors:
            raise AlreadyRegistered(spec, name)
        self.adaptors[k] = factory

    def find_factory(self, spec: Optional[type[T]] = None, *, name: str = "") -> Factory[T]:
        k = spec, name
        if k not in self.adaptors:
            raise DoesNotRegistered(spec, name)
        return cast(Factory[T], self.adaptors[k])

    def register_instance(self, instance: T, spec: Optional[type[T]] = None, *, name: str = "") -> None:
        self.register_factory(cast(Factory[T], Singleton(instance)), spec, name=name)

    def find_instance(self, spec: Optional[type[T]] = None, *, name: str = "") -> T:
        factory = self.find_factory(spec, name=name)
        if isinstance(factory, Singleton):
            return cast(T, factory.instance)
        raise IsNotSingleton(spec, name)

    def create_container(self) -> "Container":
        return Container(registry=self)


class Container:
    def __init__(self, registry: Registry) -> None:
        self.registry = registry
        self.cache: dict[tuple[Optional[type], str], Any] = {}

    def find(self, spec: Optional[type[T]] = None, *, name: str = "") -> T:
        k = spec, name
        if k not in self.cache:
            factory = self.registry.find_factory(spec, name=name)
            instance = factory(self)
            if inspect.isawaitable(instance):
                raise DoesNotSupportAwaitable(spec, name)
            self.cache[k] = instance
        return cast(T, self.cache[k])

    async def async_find(self, spec: Optional[type[T]] = None, *, name: str = "") -> T:
        k = spec, name
        if k not in self.cache:
            factory = self.registry.find_factory(spec, name=name)
            maybe_instance = factory(self)
            if inspect.isawaitable(maybe_instance):
                instance = await maybe_instance
            else:
                instance = maybe_instance
            self.cache[k] = instance
        return cast(T, self.cache[k])
