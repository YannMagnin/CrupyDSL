"""
crupydslparser.core._lexer.op_or    - lexer or operation
"""
__all__ = [
    'CrupyLexerOr',
]
from typing import List, Any

from crupydslparser.core._lexer._lexer import CrupyLexer
from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core.parser._base import CrupyParserBase
from crupydslparser.core.parser.node import CrupyParserNode

#---
# Public
#---

class CrupyLexerOr(CrupyLexer):
    """ OR lexer operation
    """
    def __init__(self, *args: Any) -> None:
        self._seq: List[CrupyLexer] = []
        for i, arg in enumerate(args):
            if CrupyLexer not in type(arg).mro():
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

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode|None:
        """ try to match at least one of the two lexer operation
        """
        for lexer in self._seq:
            if (token := lexer(parser)):
                return token
        return None
