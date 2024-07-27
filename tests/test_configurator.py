def test_include():
    from protocol_wire import Configurator, Registry

    registry = Registry()
    config = Configurator(registry)

    assert len(config.included) == 0
    config.include("example_foo")
    assert len(config.included) == 1
    config.include("example_foo")
    assert len(config.included) == 1
    config.include("example_bar")
    assert len(config.included) == 2
    config.include("example_bar")
    assert len(config.included) == 2

    from example_bar import Bar
    from example_foo import Foo

    container = registry.create_container()
    container.find(Foo)
    container.find(Bar)


def test_include_many():
    from protocol_wire import Configurator, Registry

    registry = Registry()
    config = Configurator(registry)

    assert len(config.included) == 0
    config.include_many(["example_foo", "example_bar"])
    assert len(config.included) == 2


def test_include_many_override():
    from protocol_wire import Configurator, Registry

    registry = Registry()
    config = Configurator(registry)

    assert len(config.included) == 0
    config.include_many(["example_foo", "BAR"], {"BAR": "example_bar"})
    assert len(config.included) == 2
