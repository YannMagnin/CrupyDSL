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
        self.index  = index
        self.lineno = lineno
        self.column = column
        self.index_start = index

    def __gt__(self, context: CrupyStreamContext) -> bool:
        return self.index > context.index

    def __str__(self) -> str:
        info  = f"<{type(self).__name__}: "
        info += f"index={self.index}, "
        info += f"lineno={self.lineno}, "
        info += f"column={self.column}, "
        info += f"index_start={self.index_start}>"
        return info

    #---
    # Public properties
    #---

    @property
    def has_read(self) -> int:
        """ calculated the readded counter """
        return self.index - self.index_start

    #---
    # Public methods
    #---

    ## memory primitives

    def peek_char(self) -> str|None:
        """ return the current char """
        if curr := self._stream[self.index]:
            return chr(curr & 0xff)
        return None

    def read_char(self) -> str|None:
        """ read the current char and update the cursor """
        if not (curr := self.peek_char()):
            return None
        if curr == '\n':
            self.lineno += 1
            self.column  = 0
        self.index  += 1
        self.column += 1
        return curr

    ## error handling

    def generate_error_log(self) -> str:
        """ generate error context information
        """
        error = f"Stream: line {self.lineno}, column {self.column}\n"
        line_index_start = self.index - (self.column - 1)
        line_index_stop = line_index_start
        while True:
            if not (curr := self._stream[line_index_stop]):
                break
            if (curr_char := chr(curr & 0xff)) in '\r\n':
                break
            error += curr_char
            line_index_stop += 1
        error += '\n'
        while line_index_start < self.index:
            error += '~' if line_index_start >= self.index_start else ' '
            line_index_start += 1
        error += '^'
        return error

    ## context validate short-cut

    def validate(self) -> CrupyStreamContext:
        """ validate the current context
        """
        return self._stream.context_validate(self)
