"""
tests.lexer.op_builtin      - test the CrupyLexerOpBuiltin
"""
__all__ = [
    'CrupyUnittestLexerBuiltin',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._lexer import CrupyLexerOpBuiltin
from crupydslparser.core.parser import CrupyParserBase

#---
# Public
#---

class CrupyUnittestLexerBuiltin(CrupyUnittestBase):
    """ unittest suite for the crupy lexer text operation
    """

    #---
    # Public tests
    #---

    def test_alpha(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('alpha'),
        })
        parser.register_stream('aZ')
        strop0 = parser.execute('entry')
        strop1 = parser.execute('entry')
        self.assertIsNotNone(strop0)
        self.assertIsNotNone(strop1)
        if strop0 is None or strop1 is None:
            return
        self.assertEqual(strop0['name'], 'lex_text')
        self.assertEqual(strop1['name'], 'lex_text')
        self.assertEqual(strop0['text'], 'a')
        self.assertEqual(strop1['text'], 'Z')
        self.assertIsNone(parser.execute('entry'))

    def test_digit(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('digit'),
        })
        parser.register_stream('09A')
        strop0 = parser.execute('entry')
        strop1 = parser.execute('entry')
        self.assertIsNotNone(strop0)
        self.assertIsNotNone(strop1)
        if strop0 is None or strop1 is None:
            return
        self.assertEqual(strop0['name'], 'lex_text')
        self.assertEqual(strop1['name'], 'lex_text')
        self.assertEqual(strop0['text'], '0')
        self.assertEqual(strop1['text'], '9')
        self.assertIsNone(parser.execute('entry'))
