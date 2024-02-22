"""
crupydslparser.core.stream.strea     - crupy stream abstraction
"""
# Since we should support the CPython 3.8 which does not expose the 'Self'
# type needed for the `__enter__` magic method, we use this workaround to
# allow using the class name as return type before the said class is
# finished to be declared (same behaviours than the 'Self' type)
from __future__ import annotations

__all__ = [
    'CrupyStream',
]
from typing import Any, IO, List
from mmap import mmap, ACCESS_READ, ACCESS_WRITE
from dataclasses import dataclass

from crupydslparser.core._stream.context import CrupyStreamContext
from crupydslparser.core._stream.exception import CrupyStreamException
from crupydslparser.core._stream.lexem import CrupyStreamLexem

#---
# Internals
#---

@dataclass
class _CrupyStreamContextState():
    """ crupy stream context state """
    validated:  bool
    context:    CrupyStreamContext

#---
# Public
#---

class CrupyStream():
    """ crupy input stream abstraction
    """

    #---
    # Factory methods
    #---

    @classmethod
    def from_string(cls, text: str) -> CrupyStream:
        """ create a CrupyStream for an string input """
        memory_area = mmap(
            fileno  = -1,
            length  = len(text),
            access  = ACCESS_READ | ACCESS_WRITE,
        )
        memory_area.seek(0)
        memory_area.write(bytes(text, encoding='utf8'))
        return CrupyStream(memory_area)

    @classmethod
    def from_file(cls, file: IO[str]) -> CrupyStream:
        """ create a CrupyStream for a file """
        return CrupyStream(
            mmap(
                fileno  = file.fileno(),
                length  = 0,
                access  = ACCESS_READ
            ),
        )

    @classmethod
    def from_any(cls, stream: IO[str]|str) -> CrupyStream:
        """ nexus for file or string """
        if isinstance(stream, str):
            return cls.from_string(stream)
        return cls.from_file(stream)

    #---
    # Object magic
    #---

    def __init__(self, memory_area: mmap) -> None:
        """ initialise our attribute
        """
        self._context_stack: List[_CrupyStreamContextState] = []
        self._context = CrupyStreamContext(
            index   = 0,
            lineno  = 1,
            column  = 1,
        )
        self._memory_area = memory_area
        self._memory_area.seek(0)
        self._memory_area_size = len(memory_area)
        if self._memory_area_size < 1:
            raise CrupyStreamException('Given memory area is too small')

    def __del__(self) -> None:
        """ do not forget the close the memory area
        """
        self._memory_area.close()

    #---
    # Magic context handling using `with` keyword
    #---

    def __enter__(self) -> CrupyStreamLexem:
        """ pop the current cursor context
        """
        self.context_save()
        return CrupyStreamLexem(self)

    def __exit__(self, _: Any, __: Any, ___: Any) -> None:
        """ restore the previous cursor context if not validated
        """
        self.context_restore()

    #---
    # Internal methods
    #---

    def _context_restore(self, context: CrupyStreamContext) -> None:
        """ restore the current context
        """
        self._context.index     = context.index
        self._context.lineno    = context.lineno
        self._context.column    = context.column

    #---
    # Public methods
    #---

    ## context handling

    def context_save(self) -> None:
        """ push the current context to the stack
        """
        self._context_stack.append(
            _CrupyStreamContextState(
                context     = self.context_copy(),
                validated   = False,
            )
        )

    def context_copy(self) -> CrupyStreamContext:
        """ return the current context """
        return CrupyStreamContext(
            index   = self._context.index,
            lineno  = self._context.lineno,
            column  = self._context.column,
        )

    def context_restore(self) -> None:
        """ restore the saved context
        """
        if not self._context_stack:
            raise CrupyStreamException('context_restore(): empty stack')
        context_state = self._context_stack[-1]
        if not context_state.validated:
            self._context_restore(context_state.context)
        self._context_stack.pop()

    def context_validate(self) -> CrupyStreamContext:
        """ validate the current contex
        """
        if not self._context_stack:
            raise CrupyStreamException('context_validate(): empty stack')
        self._context_stack[-1].validated = True
        return self.context_copy()

    ## peek primitives

    def peek_char(self) -> str|None:
        """ return the current char """
        if self._context.index < self._memory_area_size:
            return chr(self._memory_area[self._context.index] & 0xff)
        return None

    ## read primitives

    def read_char(self) -> str|None:
        """ read the current char and update the cursor """
        if not (curr := self.peek_char()):
            return None
        if curr == '\n':
            self._context.lineno += 1
            self._context.column  = 0
        self._context.index  += 1
        self._context.column += 1
        return curr
