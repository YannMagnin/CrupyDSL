"""
tests.lexer.op_until     - test the CrupyLexerOpUntil
"""
__all__ = (
    'CrupyUnittestLexerBetween',
)

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.parser import CrupyParserBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpBetween,
    CrupyLexerOpBetweenException,
)

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

    def test_error(self) -> None:
        """ error check """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBetween('"'),
        })
        parser.register_stream('"abcdef ijkl')
        self.assertRaises(
            cls_exc = CrupyLexerOpBetweenException,
            request = (parser, 'execute', 'entry'),
            error   = \
                'Stream: line 1, column 13\n'
                '"abcdef ijkl\n'
                '~~~~~~~~~~~~^\n'
                'CrupyLexerOpBetweenException: Reached end-of-file'
        )
        try:
            parser.execute('entry')
            self.assertAlways('production entry has been exectued')
        except CrupyLexerOpBetweenException as err:
            self.assertEqual(err.step, 1)
            self.assertEqual(err.reason, 'reached end-of-file')
