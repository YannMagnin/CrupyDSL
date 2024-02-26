"""
crupydslparser.core._lexer._operation.optional  - optional operation
"""
__all__ = [
    'CrupyParserNodeLexOptional',
    'CrupyLexerOpOptional',
]

from crupydslparser.core._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Optional
#---

class CrupyParserNodeLexOptional(CrupyParserNode):
    """ optional lexer information """
    node:   CrupyParserNode|None

class CrupyLexerOpOptional(CrupyLexerOpBase):
    """ optional operator
    """
    def __init__(self, lexer: CrupyLexerOpBase) -> None:
        self._operation = lexer

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode|None:
        """ catch lexer operation
        """
        return CrupyParserNodeLexOptional(
            stream_ctx  = parser.stream.context_copy(),
            node        = self._operation(parser),
        )
