"""
tests.lexer.op_builtin      - test the CrupyLexerOpBuiltin
"""
__all__ = (
    'CrupyUnittestLexerBuiltin',
)

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
        self.assertEqual(strop0.type, 'lex_text')
        self.assertEqual(strop1.type, 'lex_text')
        self.assertEqual(strop0.text, 'a')
        self.assertEqual(strop1.text, 'Z')
        # (todo) : error

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
        self.assertEqual(strop0.type, 'lex_text')
        self.assertEqual(strop1.type, 'lex_text')
        self.assertEqual(strop0.text, 'a')
        self.assertEqual(strop1.text, '6')
        self.assertEqual(strop2.text, '6')
        self.assertEqual(strop3.text, '7')
        # (todo) : error

    def test_digit(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('digit'),
        })
        parser.register_stream('09A')
        strop0 = parser.execute('entry')
        strop1 = parser.execute('entry')
        self.assertEqual(strop0.type, 'lex_text')
        self.assertEqual(strop1.type, 'lex_text')
        self.assertEqual(strop0.text, '0')
        self.assertEqual(strop1.text, '9')
        # (todo) : error

    def test_number(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('number'),
        })
        parser.register_stream('667,')
        strop0 = parser.execute('entry')
        self.assertEqual(strop0.type, 'lex_text')
        self.assertEqual(strop0.text, '667')
        # (todo) : error

    def test_space(self) -> None:
        """ test space """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('space'),
        })
        parser.register_stream(' \t\vabc')
        self.assertIsNotNone(parser.execute('entry'))
        self.assertIsNotNone(parser.execute('entry'))
        self.assertIsNotNone(parser.execute('entry'))
        with parser.stream as context:
            self.assertEqual(context.read_char(), 'a')
        # (todo) : error handling

    def test_any(self) -> None:
        """ test any builtin """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('any'),
        })
        parser.register_stream(r'a\"\\')
        node0 = parser.execute('entry')
        node1 = parser.execute('entry')
        node2 = parser.execute('entry')
        self.assertEqual(node0.type, 'lex_text')
        self.assertEqual(node0.text, 'a')
        self.assertEqual(node1.type, 'lex_text')
        self.assertEqual(node1.text, '"')
        self.assertEqual(node2.type, 'lex_text')
        self.assertEqual(node2.text, '\\')
        # (todo) : error
