"""
crupydslparser.parser._lexer._operarion.error   - throw context error
"""
__all__ = [
    'CrupyLexerOpError',
]

from crupydslparser.parser._lexer.exception import CrupyLexerException
from crupydslparser.parser._lexer._operation.base import CrupyLexerOpBase
from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser.parser import CrupyParserBase

#---
# Public
#---

class CrupyLexerErrorException(CrupyLexerException):
    """ generic lexer error exception """

class CrupyLexerOpError(CrupyLexerOpBase):
    """ end-of-file assert operation
    """
    def __init__(self, text: str) -> None:
        super().__init__()
        self._text = text

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ return True if we are in the end of the stream
        """
        with parser.stream as context:
            raise CrupyLexerErrorException(
                context = context,
                reason  = self._text
            )

    #---
    # Public methods
    #---

    def show(self, indent: int = 0) -> str:
        """ display a generic information
        """
        return f"{' ' * indent}{type(self).__name__}('{self._text}')"
