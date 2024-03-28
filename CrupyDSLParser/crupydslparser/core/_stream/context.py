"""
crupydslparser.core._stream.context     - stream context information
"""
# @note
# Used as a workaround for the cyclic-import and to allow using the
# class name as return type before the said class is finished to be
# declared
from __future__ import annotations

__all__ = (
    'CrupyStreamContext',
)
from typing import TYPE_CHECKING

# @note : Design mistake
#
# We cannot import the `CrupyStream` class since we use the
# `CrupyStreamContext` class in the `CrupyStream`. So, we are in a circular
# dependencies problem.
if TYPE_CHECKING:
    from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyStreamContext():
    """ stream context
    """
    def __init__(
        self,
        stream: CrupyStream,
        index: int,
        lineno: int,
        column: int,
    ) -> None:
        self._stream = stream
        self._index  = index
        self._lineno = lineno
        self._column = column
        self._readed = 0

    def __gt__(self, context: CrupyStreamContext) -> bool:
        return self._index > context._index

    #---
    # Public properties
    #---

    @property
    def index(self) -> int:
        """ return the stream index """
        return self._index

    @property
    def lineno(self) -> int:
        """ return the stream line number """
        return self._lineno

    @property
    def column(self) -> int:
        """ return the stream column """
        return self._column

    #---
    # Public methods
    #---

    ## memory primitives

    def peek_char(self) -> str|None:
        """ return the current char """
        if self._index < self._stream.size:
            return chr(self._stream[self._index] & 0xff)
        return None

    def read_char(self) -> str|None:
        """ read the current char and update the cursor """
        if not (curr := self.peek_char()):
            return None
        if curr == '\n':
            self._lineno += 1
            self._column  = 0
        self._index  += 1
        self._column += 1
        self._readed += 1
        return curr

    ## error handling

    def generate_error_log(self) -> str:
        """ generate error context information
        """
        error = f"Stream: line {self.lineno}, column {self.column}\n"
        i = self.index - (self.column - 1)
        while i < self._stream.size:
            if (curr := chr(self._stream[i] & 0xff)) in '\r\n':
                break
            error += curr
            i += 1
        error += '\n'
        error += f"{' ' * (self.column - 1)}^"
        return error

    ## context validate short-cut

    def validate(self) -> CrupyStreamContext:
        """ validate the current context
        """
        return self._stream.context_validate(self)
