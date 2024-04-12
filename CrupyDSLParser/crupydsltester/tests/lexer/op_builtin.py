"""
tests.lexer.op_builtin      - test the CrupyLexerOpBuiltin
"""
__all__ = (
    'CrupyUnittestLexerBuiltin',
)

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.parser import CrupyParserBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpBuiltin,
    CrupyLexerException,
)

#---
# Public
#---

class CrupyUnittestLexerBuiltin(CrupyUnittestBase):
    """ unittest suite for the crupy lexer text operation
    """

    #---
    # Public tests
    #---

    def test_any(self) -> None:
        """ test any builtin """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('any'),
        })
        parser.register_stream('a\\"\\\\ \a')
        node0 = parser.execute('entry')
        node1 = parser.execute('entry')
        node2 = parser.execute('entry')
        node3 = parser.execute('entry')
        self.assertEqual(node0.type, 'lex_text')
        self.assertEqual(node0.text, 'a')
        self.assertEqual(node1.type, 'lex_text')
        self.assertEqual(node1.text, '"')
        self.assertEqual(node2.type, 'lex_text')
        self.assertEqual(node2.text, '\\')
        self.assertEqual(node3.type, 'lex_text')
        self.assertEqual(node3.text, ' ')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 7\n'
                'a\\"\\\\ \a\n'
                '      ^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "any"',
            ),
            (parser, 'execute', 'entry'),
        )

    def test_alphanum(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('alphanum'),
        })
        parser.register_stream('aZ667-')
        strop0 = parser.execute('entry')
        strop1 = parser.execute('entry')
        strop2 = parser.execute('entry')
        strop3 = parser.execute('entry')
        strop4 = parser.execute('entry')
        self.assertEqual(strop0.type, 'lex_text')
        self.assertEqual(strop1.type, 'lex_text')
        self.assertEqual(strop0.text, 'a')
        self.assertEqual(strop1.text, 'Z')
        self.assertEqual(strop2.text, '6')
        self.assertEqual(strop3.text, '6')
        self.assertEqual(strop4.text, '7')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 6\n'
                'aZ667-\n'
                '     ^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "alphanum"',
            ),
            (parser, 'execute', 'entry'),
        )

    def test_alphanum_lower(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('alphanum_lower'),
        })
        parser.register_stream('a667Z')
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
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 5\n'
                'a667Z\n'
                '    ^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "alphanum_lower"',
            ),
            (parser, 'execute', 'entry'),
        )

    def test_alphanum_upper(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('alphanum_upper'),
        })
        parser.register_stream('A667z')
        strop0 = parser.execute('entry')
        strop1 = parser.execute('entry')
        strop2 = parser.execute('entry')
        strop3 = parser.execute('entry')
        self.assertEqual(strop0.type, 'lex_text')
        self.assertEqual(strop1.type, 'lex_text')
        self.assertEqual(strop0.text, 'A')
        self.assertEqual(strop1.text, '6')
        self.assertEqual(strop2.text, '6')
        self.assertEqual(strop3.text, '7')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 5\n'
                'A667z\n'
                '    ^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "alphanum_upper"',
            ),
            (parser, 'execute', 'entry'),
        )

    def test_alpha(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('alpha'),
        })
        parser.register_stream('aZ1')
        strop0 = parser.execute('entry')
        strop1 = parser.execute('entry')
        self.assertEqual(strop0.type, 'lex_text')
        self.assertEqual(strop1.type, 'lex_text')
        self.assertEqual(strop0.text, 'a')
        self.assertEqual(strop1.text, 'Z')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 3\n'
                'aZ1\n'
                '  ^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "alpha"',
            ),
            (parser, 'execute', 'entry'),
        )

    def test_alpha_lower(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('alpha_lower'),
        })
        parser.register_stream('azZ')
        strop0 = parser.execute('entry')
        strop1 = parser.execute('entry')
        self.assertEqual(strop0.type, 'lex_text')
        self.assertEqual(strop1.type, 'lex_text')
        self.assertEqual(strop0.text, 'a')
        self.assertEqual(strop1.text, 'z')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 3\n'
                'azZ\n'
                '  ^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "alpha_lower"',
            ),
            (parser, 'execute', 'entry'),
        )

    def test_alpha_upper(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('alpha_upper'),
        })
        parser.register_stream('AZw')
        strop0 = parser.execute('entry')
        strop1 = parser.execute('entry')
        self.assertEqual(strop0.type, 'lex_text')
        self.assertEqual(strop1.type, 'lex_text')
        self.assertEqual(strop0.text, 'A')
        self.assertEqual(strop1.text, 'Z')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 3\n'
                'AZw\n'
                '  ^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "alpha_upper"',
            ),
            (parser, 'execute', 'entry'),
        )

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
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 3\n'
                '09A\n'
                '  ^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "digit"',
            ),
            (parser, 'execute', 'entry'),
        )

    def test_number(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('number'),
        })
        parser.register_stream('667,')
        strop0 = parser.execute('entry')
        self.assertEqual(strop0.type, 'lex_text')
        self.assertEqual(strop0.text, '667')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 4\n'
                '667,\n'
                '   ^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "number"',
            ),
            (parser, 'execute', 'entry'),
        )

    def test_symbol(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('symbol'),
        })
        parser.register_stream('{*\\t')
        strop0 = parser.execute('entry')
        strop1 = parser.execute('entry')
        strop2 = parser.execute('entry')
        self.assertEqual(strop0.type, 'lex_text')
        self.assertEqual(strop1.type, 'lex_text')
        self.assertEqual(strop0.text, '{')
        self.assertEqual(strop1.text, '*')
        self.assertEqual(strop2.text, '\\')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 4\n'
                '{*\\t\n'
                '   ^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "symbol"',
            ),
            (parser, 'execute', 'entry'),
        )

    def test_space(self) -> None:
        """ test space """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('space'),
        })
        parser.register_stream(' \tabc')
        self.assertIsNotNone(parser.execute('entry'))
        self.assertIsNotNone(parser.execute('entry'))
        with parser.stream as context:
            self.assertEqual(context.read_char(), 'a')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 3\n'
                ' \tabc\n'
                '        ^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "space"',
            ),
            (parser, 'execute', 'entry'),
        )

    def test_space_nl(self) -> None:
        """ test space """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('space_nl'),
            'test0' : CrupyLexerOpBuiltin('any'),
        })
        parser.register_stream(' \t\nabc')
        self.assertIsNotNone(parser.execute('entry'))
        self.assertIsNotNone(parser.execute('entry'))
        self.assertIsNotNone(parser.execute('entry'))
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 2, column 1\n'
                'abc\n'
                '^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "space_nl"',
            ),
            (parser, 'execute', 'entry'),
        )

    def test_oef(self) -> None:
        """ test space """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpBuiltin('eof'),
        })
        parser.register_stream('a')
        with parser.stream as context:
            context.read_char()
            self.assertIsNotNone(parser.execute('entry'))
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 1\n'
                'a\n'
                '^\n'
                'CrupyLexerOpBuiltin: Unable to validate the current '
                'char as "EOF", stream available',
            ),
            (parser, 'execute', 'entry'),
        )
