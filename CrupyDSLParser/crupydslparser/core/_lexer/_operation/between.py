"""
crupydslparser.core._lexer._operation.between   - Lexer between operation
"""
__all__ = (
    'CrupyParserNodeLexBetween',
    'CrupyLexerOpBetween',
)

from crupydslparser.core._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Public
#---

class CrupyParserNodeLexBetween(CrupyParserNode):
    """ string node information """
    text: str

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238
class CrupyLexerOpBetween(CrupyLexerOpBase):
    """ capture between delimiter
    """
    def __init__(self, delimiter: str) -> None:
        self._delimiter = delimiter

    def _execute(
        self,
        parser: CrupyParserBase,
        _: bool,
    ) -> CrupyParserNode|None:
        """ try to strictly match the text
        """
        with parser.stream as lexem:
            if lexem.read_char() != self._delimiter:
                return None
            content = ''
            while True:
                if not (curr := lexem.read_char()):
                    return None
                if curr == self._delimiter:
                    break
                content += curr
            return CrupyParserNodeLexBetween(
                stream_ctx  = lexem.validate(),
                text        = content,
            )
