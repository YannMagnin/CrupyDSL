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
    ) -> None:
        """ simply wrap the parser base exception and handle dataclass

        Technical notes:
        To support the `crupydataclass` decoration, we need to allow the
        `args` and `kwargs` arguments, event if not used here. This because
        the decorator will hook this constructor and drop-off all provided
        arguments (even if processed).

        (todo) : remove this limitation
        """
        super().__init__(
            reason  = f"{self.__class__.__name__}: {reason}",
            context = context,
        )
