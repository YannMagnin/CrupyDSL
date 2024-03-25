"""
crupydslparser.core._lexer._operation.choice    - lexer or operation
"""
__all__ = [
    'CrupyLexerOpOr',
]
from typing import List, Any

from crupydslparser.core._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Public
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238
class CrupyLexerOpOr(CrupyLexerOpBase):
    """ OR lexer operation
    """
    def __init__(self, *args: Any) -> None:
        self._seq: List[CrupyLexerOpBase] = []
        for i, arg in enumerate(args):
            if CrupyLexerOpBase not in type(arg).mro():
                raise CrupyLexerException(
                    f"Unable to initialise the {type(arg).__name__} "
                    f"because the argument {i} is not of type "
                    f"CrupyLexerOpBase ({type(arg).__name__})"
                )
            self._seq.append(arg)
        if not self._seq:
            raise CrupyLexerException(
                f"Unable to initialise the {self.__class__.__name__} "
                "because not sequence has been presented"
            )

    def _execute(
        self,
        parser: CrupyParserBase,
        last_chance: bool,
    ) -> CrupyParserNode|None:
        """ try to match at least one of the two lexer operation
        """
        for lexer in self._seq:
            last_chance_really = False
            if lexer == self._seq[-1]:
                last_chance_really = last_chance
            if (token := lexer(parser, last_chance_really)):
                return token
        return None
