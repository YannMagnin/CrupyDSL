"""
crupydslparser.core._lexer._assert.eof  - end-of-file assert
"""
__all__ = [
    'CrupyLexerAssertEOF',
]

from crupydslparser.core._lexer._assert._base import CrupyLexerAssertBase
from crupydslparser.core.parser import CrupyParserBase

#---
# Public
#---

class CrupyLexerAssertEOF(CrupyLexerAssertBase):
    """ end-of-file assert operation
    """
    def __call__(self, parser: CrupyParserBase) -> bool:
        """ return True if we are in the end of the stream
        """
        return parser.stream.peek_char() is None
