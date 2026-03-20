from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SaludoRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class SaludoResponse(_message.Message):
    __slots__ = ("mensaje",)
    MENSAJE_FIELD_NUMBER: _ClassVar[int]
    mensaje: str
    def __init__(self, mensaje: _Optional[str] = ...) -> None: ...
