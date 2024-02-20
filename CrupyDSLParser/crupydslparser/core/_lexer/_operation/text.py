"""
crupydslparser.core._lexer._operation.text  - Lexer text tool
"""
__all__ = [
    'CrupyParserNodeLexText',
    'CrupyLexerOpText',
]

from crupydslparser.core._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.core.parser._base import CrupyParserBase
from crupydslparser.core.parser.node import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeLexText(CrupyParserNode):
    """ string token information """
    text: str

class CrupyLexerOpText(CrupyLexerOpBase):
    """ strict string matcher
    """
    def __init__(self, text: str) -> None:
        self._text = text

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode|None:
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
