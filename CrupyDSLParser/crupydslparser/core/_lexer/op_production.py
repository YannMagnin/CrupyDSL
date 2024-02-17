"""
crupydslparser.core._lexer.op_rule  - lexer rule operation
"""
__all__ = [
    'CrupyLexerProduction',
]

from crupydslparser.core._lexer._lexer import CrupyLexer
from crupydslparser.core._lexer._token import CrupyLexerToken
from crupydslparser.core._parser._base import CrupyParserBase

#---
# Public
#---

class CrupyLexerProduction(CrupyLexer):
    """ Rule invocation operation
    """
    def __init__(self, production_name: str) -> None:
        self._production_name = production_name


    def __call__(self, parser: CrupyParserBase) -> CrupyLexerToken|None:
        """ invoke another production rule
        """
        return parser.execute(self._production_name)
