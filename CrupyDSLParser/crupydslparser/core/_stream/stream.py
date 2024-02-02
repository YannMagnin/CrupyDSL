"""
crupydslparser.core.stream.strea     - crupy stream abstraction
"""
# Since we should support the CPython 3.8 which does not expose the 'Self'
# type needed for the `__enter__` magic method, we use this workaround to
# allow using the class name as return type before the said class is finished
# to be declared (same behaviours than the 'Self' type)
from __future__ import annotations

__all__ = [
    'CrupyStream',
]
from typing import Any, IO
from mmap import mmap, ACCESS_READ, ACCESS_WRITE

#---
# Public
#---

class CrupyStream(mmap):
    """ crupy input stream abstraction
    """
    def __init__(self, *_: Any, **__: Any) -> None:
        """ initialise our attribute

        We don't invoke the `mmap.mmap.__init__()` primitive because mmap
        doesn't expose it. When you "initialize" this particular object
        (impletented in C under the hood), it will only firstly involve
        `mmap.mmap.__new__()` which will handle arguments passed through
        like `length=, access=<>, ...` and then involve the user
        `__init__()` methods (or `object.__init__()` depending on the
        Method Resolution Order (MRO)).

        This distinction between `__new__()` and `__init__()` are
        critical to respect the RAII idom. The idea here is to performs
        the `mmap(2)` syscall as soon as possible (before the user can
        take control) and never involve the `__init__()` if an error
        occurs during the ressource aquisition.

        This is why we do not performs any `super()` initialisation here.
        """
        self._line_counter = 0

    #---
    # Factory methods
    #---

    @classmethod
    def from_string(cls, text: str) -> CrupyStream:
        """ create a CrupyStream for an string input """
        stream = CrupyStream(
            fileno  = -1,
            lenght  = len(text),
            access  = ACCESS_READ | ACCESS_WRITE,
        )
        stream.seek(0)
        stream.write(bytes(text, encoding='utf8'))
        return stream

    @classmethod
    def from_file(cls, file: IO[str]) -> CrupyStream:
        """ create a CrupyStream for a file """
        stream = CrupyStream(
            fileno  = file.fileno(),
            lenght  = 0,
            access  = ACCESS_READ
        )
        stream.seek(0)
        return stream

    @classmethod
    def from_any(cls, stream: IO[str]|str) -> CrupyStream:
        """ nexus for file or string """
        if isinstance(stream, str):
            return cls.from_string(stream)
        return cls.from_file(stream)
