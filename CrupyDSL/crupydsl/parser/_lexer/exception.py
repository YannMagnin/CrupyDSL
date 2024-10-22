"""
crupydsl.parser._lexer.exception  - lexer exception class
"""
# allow returning `CrupyDSLLexerException` in class methods prototype since
# the type, as the time where CPython analyse the class, do not "really"
# exists
from __future__ import annotations

__all__ = [
    'CrupyDSLLexerException',
]
from typing import Optional, Any

from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.parser._stream.context import CrupyDSLStreamContext
from crupydsl._utils import (
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
class CrupyDSLLexerException(CrupyDSLParserBaseException):
    """ Crupy lexer exception class

    @notes
    - force disable the `__repr__` and `__str__` magic methods provided by
        my own dataclass, because I want to have the default behaviours of
        exception class when used like `str(err)`
    """
    def __init__(
        self,
        reason: str,
        context: CrupyDSLStreamContext,
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
