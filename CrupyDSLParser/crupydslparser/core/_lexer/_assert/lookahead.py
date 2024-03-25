"""
crupydslparser.core._lexer._assert.lookahead    - lookehader assert
"""
__all__ =[
    'CrupyLexerAssertLookaheadNegative',
    'CrupyLexerAssertLookaheadPositive',
]
from typing import List, Any

from crupydslparser.core._lexer._assert._base import CrupyLexerAssertBase
from crupydslparser.core._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core.parser import CrupyParserBase

#---
# Public
#---

class CrupyLexerAssertLookaheadNegative(CrupyLexerAssertBase):
    """ lexer lookahead negative operation
    """
    def __init__(self, *args: Any) -> None:
        self._seq: List[CrupyLexerOpBase] = []
        for i, arg in enumerate(args):
            if CrupyLexerOpBase not in type(arg).mro():
                raise CrupyLexerException(
                    'Unable to initialise the CrupyLexerSeq because the '
                    f"argument {i} is not of type CrupyLexer "
                    f"({type(arg)})"
                )
            self._seq.append(arg)
        if not self._seq:
            raise CrupyLexerException(
                'Unable to initialise the CrupyLexerSeq because not '
                'sequence has been presented'
            )

    def __call__(self, parser: CrupyParserBase) -> bool:
        """ return True of the lexer operation not match
        """
        with parser.stream as _:
            for lexer in self._seq:
                if not lexer(parser, False):
                    return True
            return False

class CrupyLexerAssertLookaheadPositive(CrupyLexerAssertLookaheadNegative):
    """ lexer lookahead negative operation
    """
    def __call__(self, parser: CrupyParserBase) -> bool:
        """ return True of the lexer operation not match
        """
        return not super().__call__(parser)
