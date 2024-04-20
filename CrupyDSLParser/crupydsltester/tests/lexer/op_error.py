"""
tests.lexer.op_error    - test the CrupyLexerOpError
"""
__all__ = (
    'CrupyUnittestLexerError',
)

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.parser import (
    CrupyParserBase,
    CrupyParserBaseException,
)
from crupydslparser.parser._lexer import (
    CrupyLexerOpError,
    CrupyLexerOpSeq,
    CrupyLexerOpOr,
    CrupyLexerOpOptional,
)

#---
# Public
#---

class CrupyUnittestLexerError(CrupyUnittestBase):
    """ unittest suite for the crupy lexer error operation
    """

    #---
    # Public tests
    #---

    def test_simple(self) -> None:
        """ simple valid case """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpError('foo bar ekip'),
        })
        try:
            parser.register_stream('aaaaaaaa')
            parser.execute('entry')
            self.assertAlways('production entry has been executed')
        except CrupyParserBaseException as err:
            self.assertEqual(err.reason, 'foo bar ekip')

    def test_in_seq(self) -> None:
        """ simple valid case """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpSeq(
                CrupyLexerOpError('foo bar ekip'),
            ),
        })
        try:
            parser.register_stream('aaaaaaaa')
            parser.execute('entry')
            self.assertAlways('production entry has been executed')
        except CrupyParserBaseException as err:
            self.assertEqual(err.reason, 'foo bar ekip')

    def test_in_or(self) -> None:
        """ simple valid case """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpOr(
                CrupyLexerOpError('foo bar ekip'),
            ),
        })
        try:
            parser.register_stream('aaaaaaaa')
            parser.execute('entry')
            self.assertAlways('production entry has been executed')
        except CrupyParserBaseException as err:
            self.assertEqual(err.reason, 'foo bar ekip')

    def test_in_optional(self) -> None:
        """ simple valid case """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpOptional(
                CrupyLexerOpError('foo bar ekip'),
            ),
        })
        try:
            parser.register_stream('aaaaaaaa')
            parser.execute('entry')
        except CrupyParserBaseException:
            self.assertAlways('production entry has raised exception')

    def test_in_seq_and_or(self) -> None:
        """ simple valid case """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpSeq(
                CrupyLexerOpOr(
                    CrupyLexerOpError('foo bar ekip'),
                ),
            ),
        })
        try:
            parser.register_stream('aaaaaaaa')
            parser.execute('entry')
            self.assertAlways('production entry has been executed')
        except CrupyParserBaseException as err:
            self.assertEqual(err.reason, 'foo bar ekip')
