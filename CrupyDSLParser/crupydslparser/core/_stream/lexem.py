"""
crupydslparser.core._stream.lexem   - lexem abstraction
"""
__all__ = [
    'CrupyStreamLexem',
]
from typing import Any

#---
# Public
#---

class CrupyStreamLexem():
    """ stream lexem abstraction
    """
    def __init__(self, stream: Any) -> None:
        self._stream = stream
        self._readed = 0

    #---
    # Public methods
    #---

    ## utils

    def validate(self) -> None:
        """ validate the context
        """
        self._stream.context_validate()

    ## read operation

    def read(self) -> str|None:
        """ return the complet lexem and update internal cursor
        """
        lexem = ''
        while (curr := self.read_char()):
            lexem += curr
        return lexem if lexem else None

    def read_char(self) -> str|None:
        """ return the current char or None if the end of lexem is reached
        """
        curr: str|None = self._stream.peek_char()
        if not curr:
            return None
        if self._stream.is_lexem_separator(curr):
            return None
        self._stream.read_char()
        return curr
