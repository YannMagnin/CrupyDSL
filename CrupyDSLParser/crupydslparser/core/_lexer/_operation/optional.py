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

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238
class CrupyLexerOpOptional(CrupyLexerOpSeq):
    """ optional operator
    """
    def _execute(
        self,
        parser: CrupyParserBase,
        _: bool,
    ) -> CrupyParserNode|None:
        """ catch lexer operation
        """
        seq = None
        if node := super()._execute(parser, False):
            seq = node.seq
        return CrupyParserNodeLexOptional(
            stream_ctx  = parser.stream.context_copy(),
            seq         = seq,
        )
