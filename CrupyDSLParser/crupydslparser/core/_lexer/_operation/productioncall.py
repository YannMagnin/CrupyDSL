"""
crupydslparser.core._lexer._operation.productioncall  - lexer rule operation
"""
__all__ = (
    'CrupyLexerOpProductionCall',
)

from crupydslparser.core._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Public
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238
class CrupyLexerOpProductionCall(CrupyLexerOpBase):
    """ Rule invocation operation
    """
    def __init__(self, production_name: str) -> None:
        self._production_name = production_name

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode:
        """ invoke another production rule
        """
        return parser.execute(self._production_name)
