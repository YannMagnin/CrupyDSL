"""
crupydslparser.parser._lexer._operation.optional  - optional operation
"""
__all__ = [
    'CrupyParserNodeLexOptional',
    'CrupyLexerOpOptional',
]

from crupydslparser.parser._lexer import CrupyLexerException
from crupydslparser.parser._lexer._operation.seq import CrupyLexerOpSeq
from crupydslparser.parser import (
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
    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode:
        """ optional lexer operation
        """
        with parser.stream as context:
            try:
                seq = super().__call__(parser).seq
            except CrupyLexerException:
                seq = None
            return CrupyParserNodeLexOptional(
                context = context.validate(),
                seq     = seq,
            )
