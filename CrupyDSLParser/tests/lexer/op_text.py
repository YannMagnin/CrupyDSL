"""
tests.lexer.op_text     - test the CrupyLexerOpText
"""
__all__ = [
    'CrupyUnittestLexerText',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core.parser import CrupyParserBase
from crupydslparser.core._lexer import (
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
            'entry2' : CrupyLexerOpText('jkc'),
            'entry3' : CrupyLexerOpText('jkl'),
        })
        parser.register_stream('abcdefijkl')
        strop0 = parser.execute('entry0', False)
        strop1 = parser.execute('entry1', False)
        strop2 = parser.execute('entry2', False)
        strop3 = parser.execute('entry3', False)
        self.assertIsNotNone(strop0)
        self.assertIsNotNone(strop1)
        self.assertIsNone(strop2)
        self.assertIsNotNone(strop3)

    def test_simple_error(self) -> None:
        """ simple error case """
        parser = CrupyParserBase({
            'entry0' : CrupyLexerOpText('abcdef'),
            'entry1' : CrupyLexerOpText('jkl'),
        })
        parser.register_stream('abcdefijkl')
        self.assertIsNotNone(parser.execute('entry0', False))
        self.assertRaises(
            CrupyLexerException(
                'Parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 7\n'
                'abcdefijkl\n'
                '      ^\n'
                '\n'
                'SyntaxError: invalid syntax (unable to find '
                'appropriate production to parse this stream here)'
            ),
            (parser, 'execute', 'entry1', True),
        )
