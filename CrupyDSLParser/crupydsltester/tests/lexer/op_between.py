"""
tests.lexer.op_until     - test the CrupyLexerOpUntil
"""
__all__ = (
    'CrupyUnittestLexerBetween',
)

from crupydsltester.unittest import CrupyUnittestBase
from crupydsltester._lexer import CrupyLexerOpBetween
from crupydsltester.parser import CrupyParserBase

#---
# Public
#---

class CrupyUnittestLexerBetween(CrupyUnittestBase):
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
        parser.register_stream('"abcdef" "ijkl')
        strop0 = parser.execute('entry')
        self.assertEqual(strop0.text, 'abcdef')
        # (todo) : error
