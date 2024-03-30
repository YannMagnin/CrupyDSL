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

# allow to few methods
# pylint: disable=locally-disabled,R0903
class CrupyLexerOpBetween(CrupyLexerOpBase):
    """ capture between delimiter
    """
    def __init__(self, delimiter: str) -> None:
        self._delimiter = delimiter

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode:
        """ try to strictly match the text
        """
        with parser.stream as context:
            if context.read_char() != self._delimiter:
                self._raise_from_context(
                    context,
                    'Unable to validate the first delimiter',
                )
            content = ''
            while True:
                if not (curr := context.read_char()):
                    self._raise_from_context(
                        context,
                        'Reached end-of-file'
                    )
                if curr == self._delimiter:
                    break
                content += curr
            return CrupyParserNodeLexBetween(
                context = context.validate(),
                text    = content,
            )
