"""
crupydslparser.core._lexer._operation.text  - Lexer text tool
"""
__all__ = (
    'CrupyParserNodeLexText',
    'CrupyLexerOpText',
)

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

# allow to few methods
# pylint: disable=locally-disabled,R0903
class CrupyLexerOpText(CrupyLexerOpBase):
    """ strict string matcher
    """
    def __init__(self, text: str) -> None:
        self._text = text

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode:
        """ try to strictly match the text
        """
        with parser.stream as context:
            for char in self._text:
                if context.read_char() != char:
                    self._raise_from_context(
                        context,
                        f"Unable to match the text '{self._text}'",
                    )
            return CrupyParserNodeLexText(
                context = context.validate(),
                text    = self._text,
            )
