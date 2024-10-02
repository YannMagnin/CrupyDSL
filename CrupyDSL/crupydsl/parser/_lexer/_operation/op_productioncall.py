"""
crupydsl.parser._lexer._operation.productioncall - lexer prod op
"""
__all__ = [
    'CrupyDSLLexerOpProductionCall',
    'CrupyDSLLexerOpProductionCallException',
]

from crupydsl.parser._lexer._operation.op_base import CrupyDSLLexerOpBase
from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser.node import CrupyDSLParserNodeBase
from crupydsl.parser._lexer.exception import CrupyDSLLexerException

#---
# Public
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

class CrupyDSLLexerOpProductionCallException(CrupyDSLLexerException):
    """ exception class """
    production: str

class CrupyDSLLexerOpProductionCall(CrupyDSLLexerOpBase):
    """ Rule invocation operation
    """
    def __init__(self, production_name: str) -> None:
        super().__init__()
        self._production_name = production_name


    def __call__(self, parser: CrupyDSLParserBase) -> CrupyDSLParserNodeBase:
        """ invoke another production rule
        """
        with parser.stream as context:
            if self._production_name not in parser.production_book:
                raise CrupyDSLLexerOpProductionCallException(
                    context     = context,
                    production  = self._production_name,
                    reason      = \
                        'unable to find the production named '
                        f"'{self._production_name}'"
                )
        node = parser.execute(self._production_name)
        return node

    #---
    # Public methods
    #---

    def show(self, indent: int = 0) -> str:
        """ display a generic information
        """
        return \
            f"{' ' * indent}{type(self).__name__}('{self._production_name}')"
