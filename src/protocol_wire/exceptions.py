class ProtocolWireError(Exception):
    pass


class AlreadyRegistered(ProtocolWireError):
    pass


class DoesNotRegistered(ProtocolWireError):
    pass


class IsNotSingleton(ProtocolWireError):
    pass


class DoesNotSupportAwaitable(ProtocolWireError):
    pass
