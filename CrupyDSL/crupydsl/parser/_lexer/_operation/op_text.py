"""
crupydsl.parser._lexer._operation.text  - Lexer text tool
"""
__all__ = [
    'CrupyDSLParserNodeLexText',
    'CrupyDSLLexerOpText',
    'CrupyDSLLexerOpTextException',
]

from crupydsl.parser._lexer._operation.op_base import CrupyDSLLexerOpBase
from crupydsl.parser._lexer.exception import CrupyDSLLexerException
from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser.node import CrupyDSLParserNodeBase

#---
# Public
#---

# allow to few methods
# pylint: disable=locally-disabled,R0903

class CrupyDSLParserNodeLexText(CrupyDSLParserNodeBase):
    """ string token information """
    text: str

class CrupyDSLLexerOpTextException(CrupyDSLLexerException):
    """ custom exception handling """
    read: int
    match: str

class CrupyDSLLexerOpText(CrupyDSLLexerOpBase):
    """ strict string matcher
    """
    def __init__(self, text: str) -> None:
        super().__init__()
        self._text = text

    def __call__(self, parser: CrupyDSLParserBase) -> CrupyDSLParserNodeBase:
        """ try to strictly match the text
        """
        with parser.stream as context:
            has_read = 0
            for char in self._text:
                if not (curr := context.peek_char()):
                    raise CrupyDSLLexerOpTextException(
                        context = context,
                        reason  = 'reached end-of-file',
                        read    = has_read,
                        match   = self._text,
                    )
                if curr != char:
                    raise CrupyDSLLexerOpTextException(
                        context = context,
                        read    = has_read,
                        match   = self._text,
                        reason  = \
                            f"unable to match the text '{self._text}'",
                    )
                context.read_char()
                has_read += 1
            return CrupyDSLParserNodeLexText(
                context = context.validate(),
                text    = self._text,
            )

    #---
    # Public methods
    #---

    def show(self, indent: int = 0) -> str:
        """ display a generic information
        """
        return f"{' ' * indent}{type(self).__name__}('{self._text}')"
