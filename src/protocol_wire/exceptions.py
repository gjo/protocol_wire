class ProtocolWireError(Exception):
    pass


class AlreadyRegisteredError(ProtocolWireError):
    pass


class DoesNotRegisteredError(ProtocolWireError):
    pass


class IsNotSingletonError(ProtocolWireError):
    pass


class DoesNotSupportAwaitableError(ProtocolWireError):
    pass


class SpecIsNotProtocolError(ProtocolWireError):
    pass
