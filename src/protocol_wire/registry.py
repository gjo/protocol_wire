import inspect
from collections.abc import Collection, Mapping
from importlib import import_module
from types import ModuleType
from typing import Any, Awaitable, Callable, Protocol, TypeVar, cast

from .exceptions import AlreadyRegistered, DoesNotRegistered, DoesNotSupportAwaitable, IsNotSingleton
from .utils import is_delivered_protocol

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


class Factory(Protocol[T_co]):
    def __call__(self, container: "Container") -> T_co | Awaitable[T_co]: ...


class Singleton(Factory[T]):
    def __init__(self, instance: T) -> None:
        self.instance = instance

    def __call__(self, contaner: "Container") -> T:
        return self.instance


class Registry:
    def __init__(self) -> None:
        self.adaptors: dict[tuple[type | None, str], Any] = {}

    def register_factory(self, factory: Factory[T], spec: type[T] | None = None, *, name: str = "") -> None:
        assert spec is None or is_delivered_protocol(spec)
        k = spec, name
        if k in self.adaptors:
            raise AlreadyRegistered(spec, name)
        self.adaptors[k] = factory

    def find_factory(self, spec: type[T] | None = None, *, name: str = "") -> Factory[T]:
        k = spec, name
        if k not in self.adaptors:
            raise DoesNotRegistered(spec, name)
        return cast(Factory[T], self.adaptors[k])

    def register_instance(self, instance: T, spec: type[T] | None = None, *, name: str = "") -> None:
        self.register_factory(cast(Factory[T], Singleton(instance)), spec, name=name)

    def find_instance(self, spec: type[T] | None = None, *, name: str = "") -> T:
        factory = self.find_factory(spec, name=name)
        if isinstance(factory, Singleton):
            return cast(T, factory.instance)
        raise IsNotSingleton(spec, name)

    def create_container(self) -> "Container":
        return Container(registry=self)


class Container:
    def __init__(self, registry: Registry) -> None:
        self.registry = registry
        self.cache: dict[tuple[type | None, str], Any] = {}

    def find(self, spec: type[T] | None = None, *, name: str = "") -> T:
        k = spec, name
        if k not in self.cache:
            factory = self.registry.find_factory(spec, name=name)
            instance = factory(self)
            if inspect.isawaitable(instance):
                raise DoesNotSupportAwaitable(spec, name)
            self.cache[k] = instance
        return cast(T, self.cache[k])

    async def async_find(self, spec: type[T] | None = None, *, name: str = "") -> T:
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


class Configurator:
    def __init__(
        self, registry: Registry, relative_base: ModuleType | None = None, entry_point: str = "includeme"
    ) -> None:
        self.registry = registry
        self.relative_base = relative_base
        self.entry_point = entry_point
        self.anchor_name = relative_base.__name__ if relative_base else None
        self.included: set[ModuleType] = set()

    def include(self, module_name: str) -> None:
        module = import_module(module_name, self.anchor_name)
        if module not in self.included:
            self.included.add(module)
            func: Callable[[Registry], None] = getattr(module, self.entry_point)
            func(self.registry)

    def include_many(self, module_names: Collection[str], overrides: Mapping[str, str] | None = None) -> None:
        if overrides is None:
            overrides = {}
        for module_name in module_names:
            if module_name in overrides:
                module_name = overrides[module_name]
            self.include(module_name)
