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
from typing import Optional, Any

from crupydslparser.parser.exception import CrupyParserBaseException
from crupydslparser.parser._stream.context import CrupyStreamContext
from crupydslparser._utils import (
    crupyabstractclass,
    crupydataclass,
)

#---
# Public
#---

@crupyabstractclass
@crupydataclass(
    enable_repr = False,
)
class CrupyLexerException(CrupyParserBaseException):
    """ Crupy lexer exception class
    """
    def __init__(
        self,
        reason: str,
        context: CrupyStreamContext,
        *_: Any,
        message: Optional[str] = None,
        **__: Any,
    ) -> None:
        """ wrap the parser exception class to force providing context
        """
        if message is None:
            message = \
                'Lexer parsing error occured:\n'    \
                '\n'                                \
                f"{context.generate_error_log()}\n" \
                f"{self.__class__.__name__}: "      \
                f"{reason[0].upper()}{reason[1:]}"
        super().__init__(
            context = context,
            reason  = reason,
            message = message,
        )
