"""
crupydslparser.core._lexer._operation.text  - Lexer text tool
"""
__all__ = [
    'CrupyParserNodeLexText',
    'CrupyLexerOpText',
]

from crupydslparser.core._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Public
#---

class CrupyParserNodeLexText(CrupyParserNode):
    """ string token information """
    text: str

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238
class CrupyLexerOpText(CrupyLexerOpBase):
    """ strict string matcher
    """
    def __init__(self, text: str) -> None:
        self._text = text

    def _execute(
        self,
        parser: CrupyParserBase,
        _: bool,
    ) -> CrupyParserNode|None:
        """ try to strictly match the text
        """
        with parser.stream as lexem:
            for char in self._text:
                if lexem.read_char() != char:
                    return None
            return CrupyParserNodeLexText(
                stream_ctx  = lexem.validate(),
                text        = self._text,
            )
