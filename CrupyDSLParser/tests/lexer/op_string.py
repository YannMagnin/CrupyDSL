"""
tests.lexer.op_text     - test the CrupyLexerText
"""
__all__ = [
    'CrupyUnittestLexerText',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._lexer import CrupyLexerText
from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyUnittestLexerText(CrupyUnittestBase):
    """ unittest suite for the crupy lexer text operation
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid cases """
        stream = CrupyStream.from_any('abcdef ijkl')
        strop0 = CrupyLexerText('abcdef')
        strop1 = CrupyLexerText('i')
        strop2 = CrupyLexerText('jkc')
        strop3 = CrupyLexerText('jkl')
        self.assertIsNotNone(strop0(stream))
        self.assertIsNotNone(strop1(stream))
        self.assertIsNone(strop2(stream))
        self.assertIsNotNone(strop3(stream))
