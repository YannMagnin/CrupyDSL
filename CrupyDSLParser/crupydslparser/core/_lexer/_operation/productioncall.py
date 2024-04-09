"""
crupydslparser.core._lexer._operation.productioncall  - lexer rule operation
"""
__all__ = [
    'CrupyLexerOpProductionCall',
]

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
        with parser.stream as context:
            if self._production_name not in parser.production_book:
                self._raise_from_context(
                    context,
                    'Unable to find the production named '
                    f"'{self._production_name}'"
                )
        return parser.execute(self._production_name)
