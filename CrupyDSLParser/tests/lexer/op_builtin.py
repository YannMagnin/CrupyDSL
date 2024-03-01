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

    def test_alphanum(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('alphanum'),
        })
        parser.register_stream('a667')
        strop0 = parser.execute('entry')
        strop1 = parser.execute('entry')
        strop2 = parser.execute('entry')
        strop3 = parser.execute('entry')
        strop4 = parser.execute('entry')
        self.assertIsNotNone(strop0)
        self.assertIsNotNone(strop1)
        self.assertIsNotNone(strop2)
        self.assertIsNotNone(strop3)
        self.assertIsNone(strop4)
        if (
               strop0 is None
            or strop1 is None
            or strop2 is None
            or strop3 is None
        ):
            return
        self.assertEqual(strop0['name'], 'lex_text')
        self.assertEqual(strop1['name'], 'lex_text')
        self.assertEqual(strop0['text'], 'a')
        self.assertEqual(strop1['text'], '6')
        self.assertEqual(strop2['text'], '6')
        self.assertEqual(strop3['text'], '7')

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

    def test_number(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('number'),
        })
        parser.register_stream('667,')
        strop0 = parser.execute('entry')
        strop1 = parser.execute('entry')
        self.assertIsNotNone(strop0)
        self.assertIsNone(strop1)
        if strop0 is None:
            return
        self.assertEqual(strop0['name'], 'lex_text')
        self.assertEqual(strop0['text'], '667')

    def test_space(self) -> None:
        """ test space """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('space'),
        })
        parser.register_stream(' \t\vabc')
        self.assertIsNotNone(parser.execute('entry'))
        self.assertIsNotNone(parser.execute('entry'))
        self.assertIsNotNone(parser.execute('entry'))
        self.assertIsNone(parser.execute('entry'))
        self.assertEqual(parser.stream.read_char(), 'a')

    def test_any(self) -> None:
        """ test any builtin """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('any'),
        })
        parser.register_stream(r'a\"\\')
        node0 = parser.execute('entry')
        node1 = parser.execute('entry')
        node2 = parser.execute('entry')
        node3 = parser.execute('entry')
        self.assertIsNotNone(node0)
        self.assertIsNotNone(node1)
        self.assertIsNotNone(node2)
        self.assertIsNone(node3)
        if node0 is None or node1 is None or node2 is None:
            return
        self.assertEqual(node0['name'], 'lex_text')
        self.assertEqual(node0['text'], 'a')
        self.assertEqual(node1['name'], 'lex_text')
        self.assertEqual(node1['text'], '"')
        self.assertEqual(node2['name'], 'lex_text')
        self.assertEqual(node2['text'], '\\')
