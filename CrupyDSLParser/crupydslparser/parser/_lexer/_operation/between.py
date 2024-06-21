"""
crupydslparser.parser._lexer._operation.between - Lexer between operation
"""
__all__ = [
    'CrupyParserNodeBaseLexBetween',
    'CrupyLexerOpBetween',
]

from crupydslparser.parser._lexer._operation.base import CrupyLexerOpBase
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser.parser._lexer.exception import CrupyLexerException

#---
# Public
#---

# allow to few methods
# pylint: disable=locally-disabled,R0903

class CrupyParserNodeBaseLexBetween(CrupyParserNodeBase):
    """ string node information """
    text: str

class CrupyLexerOpBetweenException(CrupyLexerException):
    """ custom exception handling """
    step: int

class CrupyLexerOpBetween(CrupyLexerOpBase):
    """ capture between delimiter
    """
    def __init__(self, delimiter: str) -> None:
        self._delimiter = delimiter

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ try to strictly match the text
        """
        with parser.stream as context:
            if context.read_char() != self._delimiter:
                raise CrupyLexerOpBetweenException(
                    context = context,
                    reason  = 'Unable to validate the first delimiter',
                    step    = 0,
                )
            content = ''
            while True:
                if not (curr := context.read_char()):
                    raise CrupyLexerOpBetweenException(
                        context = context,
                        reason  = 'reached end-of-file',
                        step    = 1,
                    )
                if curr == self._delimiter:
                    break
                content += curr
            return CrupyParserNodeBaseLexBetween(
                context = context.validate(),
                text    = content,
            )
