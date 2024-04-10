"""
tests.lexer.op_or   - test the CrupyLexerOpOr
"""
__all__ = (
    'CrupyUnittestLexerOr',
)

from crupydsltester.unittest import CrupyUnittestBase
from crupydsltester.parser import CrupyParserBase
from crupydsltester._lexer import (
    CrupyLexerOpOr,
    CrupyLexerOpText,
    CrupyLexerException,
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
        parser.register_stream('abcdefijkl')
        or_op = parser.execute('entry')
        self.assertEqual(or_op.text, 'abc')
        with parser.stream as context:
            for n in 'defijkl':
                self.assertEqual(context.read_char(), n)

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
        parser.register_stream('abcdefijkl')
        or_op = parser.execute('entry')
        self.assertEqual(or_op.text, 'abcdef')
        with parser.stream as context:
            for n in 'ijkl':
                self.assertEqual(context.read_char(), n)

    def test_error(self) -> None:
        """ depth error handling test """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpOr(
                CrupyLexerOpText('ax'),
                CrupyLexerOpText('abcdef'),
                CrupyLexerOpText('abcx'),
                CrupyLexerOpText('xx'),
                CrupyLexerOpText('ekip'),
            ),
        })
        parser.register_stream('abcdexxx')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 6\n'
                'abcdexxx\n'
                '~~~~~^\n'
                'CrupyLexerOpOr: Unable to find an alternative that match '
                'the provided stream. Reason:\n'
                'CrupyLexerOpText: Unable to match the text \'abcdef\''
            ),
            (parser, 'execute', 'entry'),
        )
