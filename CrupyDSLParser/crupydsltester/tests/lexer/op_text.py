"""
tests.lexer.op_text     - test the CrupyLexerOpText
"""
__all__ = [
    'CrupyUnittestLexerText',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydsltester.parser import CrupyParserBase
from crupydsltester._lexer import (
    CrupyLexerOpText,
    CrupyLexerException,
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
            CrupyLexerException(
                'Stream: line 1, column 7\n'
                'abcdefijkl\n'
                '      ^\n'
                'CrupyLexerOpText: Unable to match the text \'jkl\''
            ),
            (parser, 'execute', 'entry1'),
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
            CrupyLexerException(
                'Stream: line 1, column 11\n'
                'abcdefijkl\n'
                '      ~~~~^\n'
                'CrupyLexerOpText: Reached end-of-file'
            ),
            (parser, 'execute', 'entry1'),
        )
