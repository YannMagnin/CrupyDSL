"""
tests.lexer.op_until     - test the CrupyLexerUntil
"""
__all__ = [
    'CrupyUnittestLexerUntil',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._lexer import CrupyLexerUntil
from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyUnittestLexerUntil(CrupyUnittestBase):
    """ unittest suite for the crupy lexer text operation
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid cases """
        stream = CrupyStream.from_any('"abcdef" "ijkl')
        strop0 = CrupyLexerUntil('"')(stream)
        strop1 = CrupyLexerUntil('"')(stream)
        self.assertIsNotNone(strop0)
        self.assertIsNone(strop1)
        if not strop0:
            return
        self.assertEqual(strop0['text'], 'abcdef')
