"""
tests.lexer.op_until     - test the CrupyLexerOpUntil
"""
__all__ = [
    'CrupyUnittestLexerUntil',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._lexer import CrupyLexerOpBetween
from crupydslparser.core.parser._base import CrupyParserBase

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
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBetween('"'),
        })
        strop0 = parser.execute('entry', '"abcdef" "ijkl')
        strop1 = parser.execute('entry')
        self.assertIsNotNone(strop0)
        self.assertIsNone(strop1)
        if not strop0:
            return
        self.assertEqual(strop0['text'], 'abcdef')
