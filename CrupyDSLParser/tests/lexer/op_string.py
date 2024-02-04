"""
tests.lexer.string  - test the CrupyLexerString
"""
__all__ = [
    'CrupyUnittestLexerString',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._lexer import CrupyLexerString
from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyUnittestLexerString(CrupyUnittestBase):
    """ unittest suite for the crupy lexer string operation
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid cases """
        stream = CrupyStream.from_any('abcdef ijkl')
        strop0 = CrupyLexerString('abcdef')
        strop1 = CrupyLexerString('i')
        strop2 = CrupyLexerString('jkc')
        strop3 = CrupyLexerString('jkl')
        self.assertIsNotNone(strop0(stream))
        self.assertIsNotNone(strop1(stream))
        self.assertIsNone(strop2(stream))
        self.assertIsNotNone(strop3(stream))
