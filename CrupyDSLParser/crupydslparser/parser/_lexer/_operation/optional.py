"""
crupydslparser.parser._lexer._operation.optional  - optional operation
"""
__all__ = [
    'CrupyParserNodeBaseLexOptional',
    'CrupyLexerOpOptional',
]

from crupydslparser.parser._lexer.exception import CrupyLexerException
from crupydslparser.parser._lexer._operation.seq import CrupyLexerOpSeq
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser.node import CrupyParserNodeBase

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
            except CrupyLexerException:
                seq = None
            return CrupyParserNodeLexOptional(
                context = context.validate(),
                seq     = seq,
            )
