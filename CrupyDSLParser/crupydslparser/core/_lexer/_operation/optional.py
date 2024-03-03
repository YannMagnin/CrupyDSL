"""
crupydslparser.core._lexer._operation.optional  - optional operation
"""
__all__ = [
    'CrupyParserNodeLexOptional',
    'CrupyLexerOpOptional',
]

from crupydslparser.core._lexer._operation.seq import CrupyLexerOpSeq
from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Optional
#---

class CrupyParserNodeLexOptional(CrupyParserNode):
    """ optional lexer information """
    seq:    list[CrupyParserNode]|None

class CrupyLexerOpOptional(CrupyLexerOpSeq):
    """ optional operator
    """
    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode|None:
        """ catch lexer operation
        """
        seq = None
        if node := super().__call__(parser):
            seq = node.seq
        return CrupyParserNodeLexOptional(
            stream_ctx  = parser.stream.context_copy(),
            seq         = seq,
        )
