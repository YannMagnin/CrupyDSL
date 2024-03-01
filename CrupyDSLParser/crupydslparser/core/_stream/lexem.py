"""
crupydslparser.core._stream.lexem   - lexem abstraction
"""
# @note
# Used as a workaround for the cyclic-import with the `CrupyLexer` class
from __future__ import annotations

__all__ = [
    'CrupyStreamLexem',
]
from typing import TYPE_CHECKING

from crupydslparser.core._stream.context import CrupyStreamContext

# @note : Design mistake
#
# We cannot import the `CrupyLexer` class since the magical `__call__()`
# method take a `CrupyParserBase` class as a its first argument (which is
# defined here. So, we are in a circular dependencies problem.
#
# For now, I use a combination of workarounds to by-pass this bad design
# limitation:
# - use the `TYPE_CHECKING` indicator to know if we are in checking mode
# - use the `annotations` import to allow "not well defined class"
# - import the missing `CrupyLexer` type
if TYPE_CHECKING:
    from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyStreamLexem():
    """ stream lexem abstraction
    """
    def __init__(self, stream: CrupyStream) -> None:
        self._stream = stream
        self._stream_ctx = stream.context_copy()
        self._readed = 0

    #---
    # Public methods
    #---

    ## utils

    def validate(self) -> CrupyStreamContext:
        """ validate the context and return a copy of the current context
        """
        self._stream.context_validate()
        return self._stream_ctx

    ## read operation

    def read(self) -> str|None:
        """ return the complet lexem and update internal cursor
        """
        lexem = ''
        while (curr := self.read_char()):
            lexem += curr
            self._readed += 1
        return lexem if lexem else None

    def read_char(self) -> str|None:
        """ return the current char or None if the end of lexem is reached
        """
        curr = self._stream.read_char()
        self._readed += 1
        return curr

    def peek_char(self) -> str|None:
        """ return the current char without consuming stream
        """
        return self._stream.peek_char()
