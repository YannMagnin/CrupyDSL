"""
crupydslparser.core._lexer.op_rule  - lexer rule operation
"""
__all__ = [
    'CrupyLexerProduction',
]

from crupydslparser.core._lexer._lexer import CrupyLexer
from crupydslparser.core.parser._base import CrupyParserBase
from crupydslparser.core.parser.node import CrupyParserNode

#---
# Public
#---

class CrupyLexerProduction(CrupyLexer):
    """ Rule invocation operation
    """
    def __init__(self, production_name: str) -> None:
        self._production_name = production_name

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode|None:
        """ invoke another production rule
        """
        return parser.execute(self._production_name)
