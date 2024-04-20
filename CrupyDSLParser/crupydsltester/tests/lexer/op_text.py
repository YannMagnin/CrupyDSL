"""
tests.lexer.op_text     - test the CrupyLexerOpText
"""
__all__ = [
    'CrupyUnittestLexerText',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.parser import CrupyParserBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpText,
    CrupyLexerOpTextException,
)

#---
# Public
#---

class CrupyUnittestLexerText(CrupyUnittestBase):
    """ unittest suite for the crupy lexer text operation
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry0' : CrupyLexerOpText('abcdef'),
            'entry1' : CrupyLexerOpText('i'),
            'entry3' : CrupyLexerOpText('jkl'),
        })
        parser.register_stream('abcdefijkl')
        strop0 = parser.execute('entry0')
        strop1 = parser.execute('entry1')
        strop3 = parser.execute('entry3')
        self.assertIsNotNone(strop0)
        self.assertIsNotNone(strop1)
        self.assertIsNotNone(strop3)

    def test_simple_error(self) -> None:
        """ simple error case """
        parser = CrupyParserBase({
            'entry0' : CrupyLexerOpText('abcdef'),
            'entry1' : CrupyLexerOpText('jkl'),
        })
        parser.register_stream('abcdefijkl')
        self.assertIsNotNone(parser.execute('entry0'))
        self.assertRaises(
            cls_exc = CrupyLexerOpTextException,
            request = (parser, 'execute', 'entry1'),
            error   = \
                'Lexer parsing error occured:\n'
                '\n'
                'Stream: line 1, column 7\n'
                'abcdefijkl\n'
                '      ^\n'
                'CrupyLexerOpTextException: Unable to match the text '
                '\'jkl\'',
        )
        try:
            parser.execute('entry1')
            self.assertAlways('production entry1 has been executed')
        except CrupyLexerOpTextException as err:
            self.assertEqual(err.read, 0)
            self.assertEqual(err.match, 'jkl')
            self.assertEqual(
                err.reason,
                'unable to match the text \'jkl\'',
            )

    def test_eof_error(self) -> None:
        """ test EOF handling """
        parser = CrupyParserBase({
            'entry0' : CrupyLexerOpText('abcdef'),
            'entry1' : CrupyLexerOpText('ijklm'),
        })
        parser.register_stream('abcdefijkl')
        self.assertIsNotNone(parser.execute('entry0'))
        self.assertRaises(
            cls_exc = CrupyLexerOpTextException,
            request = (parser, 'execute', 'entry1'),
            error   = \
                'Lexer parsing error occured:\n'
                '\n'
                'Stream: line 1, column 11\n'
                'abcdefijkl\n'
                '      ~~~~^\n'
                'CrupyLexerOpTextException: Reached end-of-file',
        )
