"""
crupydslparser.parser._lexer._operation.productioncall - lexer prod op
"""
__all__ = [
    'CrupyLexerOpProductionCall',
    'CrupyLexerOpProductionCallException',
]

from crupydslparser.parser._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser.parser._lexer.exception import CrupyLexerException

#---
# Public
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

class CrupyLexerOpProductionCallException(CrupyLexerException):
    """ exception class """
    production: str

class CrupyLexerOpProductionCall(CrupyLexerOpBase):
    """ Rule invocation operation
    """
    def __init__(self, production_name: str) -> None:
        self._production_name = production_name

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ invoke another production rule
        """
        with parser.stream as context:
            if self._production_name not in parser.production_book:
                raise CrupyLexerOpProductionCallException(
                    context     = context,
                    production  = self._production_name,
                    reason      = \
                        'unable to find the production named '
                        f"'{self._production_name}'"
                )
        return parser.execute(self._production_name)
