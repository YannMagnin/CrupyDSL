"""
tests.lexer.op_or   - test the CrupyLexerOpOr
"""
__all__ = [
    'CrupyUnittestLexerOr',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core.parser._base import CrupyParserBase
from crupydslparser.core._lexer import (
    CrupyLexerOpOr,
    CrupyLexerOpText,
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
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpOr(
                CrupyLexerOpText('abc'),
                CrupyLexerOpText('abcdef'),
            ),
        })
        or_op = parser.execute('entry', 'abcdef ijkl')
        self.assertIsNotNone(or_op)
        if or_op is None:
            return
        self.assertEqual(or_op['text'], 'abc')
        with parser.stream as lexem:
            self.assertEqual(lexem.read(), 'def')

    def test_simple_success1(self) -> None:
        """ simple valid case """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpOr(
                CrupyLexerOpText('zzz'),
                CrupyLexerOpText('zzz'),
                CrupyLexerOpText('zzz'),
                CrupyLexerOpText('zzz'),
                CrupyLexerOpText('abcdef'),
            ),
        })
        or_op = parser.execute('entry', 'abcdef ijkl')
        self.assertIsNotNone(or_op)
        if or_op is None:
            return
        self.assertEqual(or_op['text'], 'abcdef')
        with parser.stream as lexem:
            self.assertEqual(lexem.read(), 'ijkl')
