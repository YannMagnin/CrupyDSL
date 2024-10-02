"""
crupydsl.parser._lexer._operation.optional  - optional operation
"""
__all__ = [
    'CrupyDSLParserNodeLexOptional',
    'CrupyDSLLexerOpOptional',
]
from typing import Union

from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser.node import CrupyDSLParserNodeBase
from crupydsl.parser._lexer._operation.op_seq import (
    CrupyDSLLexerOpSeq,
    CrupyDSLLexerOpSeqException,
)

#---
# Optional
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

class CrupyDSLParserNodeLexOptional(CrupyDSLParserNodeBase):
    """ optional lexer information """
    seq: Union[list[CrupyDSLParserNodeBase],None]

class CrupyDSLLexerOpOptional(CrupyDSLLexerOpSeq):
    """ optional operator
    """
    def __call__(self, parser: CrupyDSLParserBase) -> CrupyDSLParserNodeBase:
        """ optional lexer operation
        """
        with parser.stream as context:
            try:
                seq = super().__call__(parser).seq
            except CrupyDSLLexerOpSeqException:
                seq = None
            return CrupyDSLParserNodeLexOptional(
                context = context.validate(),
                seq     = seq,
            )
