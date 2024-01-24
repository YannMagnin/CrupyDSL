"""
crupy.core.stream.strea     - crupy stream abstraction
"""
__all__ = [
    'CrupyStream',
]
from typing import Any
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
    def from_string(cls, text: str) -> Any:
        """ create a CrupyStream for an string input """
        stream = CrupyStream(
            fileno  = -1,
            lenght  = len(text),
            access  = ACCESS_READ | ACCESS_WRITE,
        )
        stream.seek(0)
        stream.write(bytes(text, encoding='utf8'))
        return stream
