"""
crupydslparser.parser._lexer._assert.eof  - end-of-file assert
"""
__all__ = [
    'CrupyLexerAssertEOF',
]

from crupydslparser.parser._lexer._assert._base import CrupyLexerAssertBase
from crupydslparser.parser import CrupyParserBase

#---
# Public
#---

class CrupyLexerAssertEOF(CrupyLexerAssertBase):
    """ end-of-file assert operation
    """
    def __call__(self, parser: CrupyParserBase) -> bool:
        """ return True if we are in the end of the stream
        """
        with parser.stream as context:
            return context.peek_char() is None