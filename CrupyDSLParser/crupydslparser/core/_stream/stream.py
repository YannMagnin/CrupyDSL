"""
crupydslparser.core.stream.strea     - crupy stream abstraction
"""
# We use this workaround to allow using the class name as return type before
# the said class is finished to be declared (same behaviours than the
# 'Self' type, but it's more explicit)
from __future__ import annotations

__all__ = (
    'CrupyStream',
)
from typing import Any, IO
from mmap import mmap, ACCESS_READ, ACCESS_WRITE
from dataclasses import dataclass

from crupydslparser.core._stream.context import CrupyStreamContext
from crupydslparser.core._stream.exception import CrupyStreamException

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
        self._context_stack: list[_CrupyStreamContextState] = []
        self._context = {
            'index'  : 0,
            'lineno' : 1,
            'column' : 1,
        }
        self._memory_area = memory_area
        self._memory_area.seek(0)
        self._memory_area_size = len(memory_area)
        if self._memory_area_size < 1:
            raise CrupyStreamException('Given memory area is too small')

    def __del__(self) -> None:
        """ do not forget the close the memory area
        """
        self._memory_area.close()

    def __getitem__(self, idx: int) -> int:
        """ do not expose directly the memory mapping
        """
        return self._memory_area[idx]

    #---
    # Magic context handling using `with` keyword
    #---

    def __enter__(self) -> CrupyStreamContext:
        """ pop the current cursor context
        """
        return self.context_push()

    def __exit__(self, _: Any, __: Any, ___: Any) -> None:
        """ restore the previous cursor context if not validated
        """
        self.context_pop()

    #---
    # Public properties
    #---

    @property
    def size(self) -> int:
        """ return the memory area size """
        return self._memory_area_size

    #---
    # Public methods
    #---

    def context_push(self) -> CrupyStreamContext:
        """ push the current context to the stack
        """
        context_new = CrupyStreamContext(
            stream  = self,
            index   = self._context['index'],
            lineno  = self._context['lineno'],
            column  = self._context['column'],
        )
        self._context_stack.append(
            _CrupyStreamContextState(
                context     = context_new,
                validated   = False,
            )
        )
        return context_new

    def context_pop(self) -> None:
        """ restore the saved context
        """
        if not self._context_stack:
            raise CrupyStreamException('context_restore(): empty stack')
        if not self._context_stack[-1].validated:
            context_new = self._context_stack[-1].context
            self._context['index']  = context_new.index
            self._context['lineno'] = context_new.lineno
            self._context['column'] = context_new.column
        self._context_stack.pop()

    def context_validate(
        self,
        context: CrupyStreamContext,
    ) -> CrupyStreamContext:
        """ validate the current context
        """
        if not self._context_stack:
            raise CrupyStreamException('context_validate(): empty stack')
        if self._context_stack[-1].context != context:
            raise CrupyStreamException(
                'context_validate(): mismatch context'
            )
        self._context_stack[-1].validated = True
        return context
