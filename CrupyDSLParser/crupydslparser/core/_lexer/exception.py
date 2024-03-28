"""
crupydslparser.core._lexer.exception     - lexer exception class
"""
# allow returning `CrupyLexerException` in class methods prototype since
# the type, as the time where CPython analyse the class, do not "really"
# exists
from __future__ import annotations

__all__ = (
    'CrupyLexerException',
)
from typing import Optional

from crupydslparser.core._stream import CrupyStreamContext
from crupydslparser.core.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyLexerException(CrupyDSLCoreException):
    """ Crupy lexer exception class """
    def __init__(
        self,
        message: str,
        context: Optional[CrupyStreamContext] = None,
    ) -> None:
        if context:
            message = f"{context.generate_error_log()}\n{message}"
        super().__init__(message)
        self._context = context

    #---
    # Properties
    #---

    @property
    def context(self) -> CrupyStreamContext:
        """ retrurn the stream context
        """
        if self._context is not None:
            return self._context
        raise CrupyDSLCoreException(
            'Accessing stream non existing stream context in lexer '
            'exception'
        )
