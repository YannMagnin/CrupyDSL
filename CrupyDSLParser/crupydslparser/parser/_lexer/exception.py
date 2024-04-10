"""
crupydslparser.parser._lexer.exception  - lexer exception class
"""
# allow returning `CrupyLexerException` in class methods prototype since
# the type, as the time where CPython analyse the class, do not "really"
# exists
from __future__ import annotations

__all__ = [
    'CrupyLexerException',
]
from typing import Optional

from crupydslparser.parser._stream import CrupyStreamContext
from crupydslparser.parser.exception import CrupyParserException

#---
# Public
#---

class CrupyLexerException(CrupyParserException):
    """ Crupy lexer exception class """
    def __init__(
        self,
        message: str,
        context: Optional[CrupyStreamContext] = None,
    ) -> None:
        reason = message
        if context:
            message = f"{context.generate_error_log()}\n{message}"
        super().__init__(message)
        self._context = context
        self._reason = reason

    #---
    # Properties
    #---

    @property
    def context(self) -> CrupyStreamContext:
        """ retrurn the stream context
        """
        if self._context is not None:
            return self._context
        raise CrupyParserException(
            'Accessing stream non existing stream context in lexer '
            'exception'
        )

    @property
    def reason(self) -> str:
        """ return the reason of the exception
        """
        return self._reason
