"""
crupydsl.parser._lexer._operation.optional  - optional operation
"""
__all__ = [
    'CrupyParserNodeLexOptional',
    'CrupyLexerOpOptional',
]
from typing import Union

from crupydsl.parser.base import CrupyParserBase
from crupydsl.parser.node import CrupyParserNodeBase
from crupydsl.parser._lexer._operation.op_seq import (
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
    seq: Union[list[CrupyParserNodeBase],None]

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
