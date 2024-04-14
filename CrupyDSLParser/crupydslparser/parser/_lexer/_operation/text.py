"""
crupydslparser.parser._lexer._operation.text  - Lexer text tool
"""
__all__ = [
    'CrupyParserNodeLexText',
    'CrupyLexerOpText',
]

from crupydslparser.parser._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.parser._lexer.exception import CrupyLexerException
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser.node import CrupyParserNodeBase

#---
# Public
#---

# allow to few methods
# pylint: disable=locally-disabled,R0903

class CrupyParserNodeLexText(CrupyParserNodeBase):
    """ string token information """
    text: str

class CrupyLexerOpTextException(CrupyLexerException):
    """ custom exception handling """
    read: int
    match: str

class CrupyLexerOpText(CrupyLexerOpBase):
    """ strict string matcher
    """
    def __init__(self, text: str) -> None:
        self._text = text

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ try to strictly match the text
        """
        with parser.stream as context:
            has_read = 0
            for char in self._text:
                if not (curr := context.peek_char()):
                    raise CrupyLexerOpTextException(
                        context = context,
                        reason  = 'Reached end-of-file',
                        read    = has_read,
                        match   = self._text,
                    )
                if curr != char:
                    raise CrupyLexerOpTextException(
                        context = context,
                        read    = has_read,
                        match   = self._text,
                        reason  = \
                            f"Unable to match the text '{self._text}'",
                    )
                context.read_char()
                has_read += 1
            return CrupyParserNodeLexText(
                context = context.validate(),
                text    = self._text,
            )