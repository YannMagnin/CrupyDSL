"""
crupydslparser.parser._lexer._operation.text  - Lexer text tool
"""
__all__ = [
    'CrupyParserNodeBaseLexText',
    'CrupyLexerOpText',
]

from crupydslparser.parser._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.parser import (
    CrupyParserBase,
    CrupyParserNodeBase,
)

#---
# Public
#---

class CrupyParserNodeBaseLexText(CrupyParserNodeBase):
    """ string token information """
    text: str

# allow to few methods
# pylint: disable=locally-disabled,R0903
class CrupyLexerOpText(CrupyLexerOpBase):
    """ strict string matcher
    """
    def __init__(self, text: str) -> None:
        self._text = text

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ try to strictly match the text
        """
        with parser.stream as context:
            for char in self._text:
                if not (curr := context.peek_char()):
                    self._raise_from_context(
                        context,
                        'Reached end-of-file',
                    )
                if curr != char:
                    self._raise_from_context(
                        context,
                        f"Unable to match the text '{self._text}'",
                    )
                context.read_char()
            return CrupyParserNodeBaseLexText(
                context = context.validate(),
                text    = self._text,
            )
