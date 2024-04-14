"""
tests.lexer.op_or   - test the CrupyLexerOpOr
"""
__all__ = (
    'CrupyUnittestLexerOr',
)

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.parser import CrupyParserBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpOr,
    CrupyLexerOpOrException,
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
            cls_exc = CrupyLexerOpOrException,
            request = (parser, 'execute', 'entry'),
            error   = \
                'Stream: line 1, column 6\n'
                'abcdexxx\n'
                '~~~~~^\n'
                'CrupyLexerOpOrException: Unable to find an alternative '
                'that match the provided stream. Reason: unable to match '
                'the text \'abcdef\''
        )
        try:
            parser.execute('entry')
            self.assertAlways('production entry has been executed')
        except CrupyLexerOpOrException as err:
            self.assertIsNotNone(err.deepest_error)
            self.assertEqual(
                err.reason,
                'unable to find an alternative that match the provided '
                'stream. Reason: unable to match the text \'abcdef\''
            )
