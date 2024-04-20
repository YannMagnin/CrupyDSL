"""
crupydslparser.parser._lexer._operation.optional  - optional operation
"""
__all__ = [
    'CrupyParserNodeLexOptional',
    'CrupyLexerOpOptional',
]

from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser.parser._lexer._operation.seq import (
    CrupyLexerOpSeq,
    CrupyLexerOpSeqException,
)

#---
# Optional
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

class CrupyParserNodeLexOptional(CrupyParserNodeBase):
    """ optional lexer information """
    seq: list[CrupyParserNodeBase]|None

class CrupyLexerOpOptional(CrupyLexerOpSeq):
    """ optional operator
    """
    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ optional lexer operation
        """
        with parser.stream as context:
            try:
                seq = super().__call__(parser).seq
            except CrupyLexerOpSeqException:
                seq = None
            return CrupyParserNodeLexOptional(
                context = context.validate(),
                seq     = seq,
            )
