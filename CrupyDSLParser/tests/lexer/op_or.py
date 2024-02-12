"""
tests.lexer.op_or   - test the CrupyLexerOr
"""
__all__ = [
    'CrupyUnittestLexerOr',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._stream import CrupyStream
from crupydslparser.core._lexer import (
    CrupyLexerOr,
    CrupyLexerText,
)

#---
# Public
#---

class CrupyUnittestLexerOr(CrupyUnittestBase):
    """ unittest suite for the crupy lexer OR operation
    """

    #---
    # Public tests
    #---

    def test_simple_success0(self) -> None:
        """ simple valid case """
        stream = CrupyStream.from_any('abcdef ijkl')
        oroper = CrupyLexerOr(
            CrupyLexerText('abc'),
            CrupyLexerText('abcdef'),
        )(stream)
        self.assertIsNotNone(oroper)
        if oroper is None:
            return
        self.assertEqual(oroper['text'], 'abc')
        with stream as lexem:
            self.assertEqual(lexem.read(), 'def')

    def test_simple_success1(self) -> None:
        """ simple valid case """
        stream = CrupyStream.from_any('abcdef ijkl')
        oroper = CrupyLexerOr(
            CrupyLexerText('zzz'),
            CrupyLexerText('zzz'),
            CrupyLexerText('zzz'),
            CrupyLexerText('zzz'),
            CrupyLexerText('abcdef'),
        )(stream)
        self.assertIsNotNone(oroper)
        if oroper is None:
            return
        self.assertEqual(oroper['text'], 'abcdef')
        with stream as lexem:
            self.assertEqual(lexem.read(), 'ijkl')
