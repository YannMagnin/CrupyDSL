"""
crupydsl.parser._lexer._operarion.error   - throw context error
"""
__all__ = [
    'CrupyDSLLexerOpError',
    'CrupyDSLLexerErrorException',
]

from crupydsl.parser._lexer.exception import CrupyDSLLexerException
from crupydsl.parser._lexer._operation.op_base import CrupyDSLLexerOpBase
from crupydsl.parser.node import CrupyDSLParserNodeBase
from crupydsl.parser import CrupyDSLParserBase

#---
# Public
#---

class CrupyDSLLexerErrorException(CrupyDSLLexerException):
    """ generic lexer error exception """

class CrupyDSLLexerOpError(CrupyDSLLexerOpBase):
    """ end-of-file assert operation
    """
    def __init__(self, text: str) -> None:
        super().__init__()
        self._text = text

    def __call__(self, parser: CrupyDSLParserBase) -> CrupyDSLParserNodeBase:
        """ return True if we are in the end of the stream
        """
        with parser.stream as context:
            raise CrupyDSLLexerErrorException(
                context = context,
                reason  = self._text
            )

    #---
    # Public methods
    #---

    def debug_show(self, indent: int = 0) -> str:
        """ display a generic information
        """
        return f"{' ' * indent}{type(self).__name__}('{self._text}')"
