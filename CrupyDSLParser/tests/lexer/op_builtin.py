"""
tests.lexer.op_builtin      - test the CrupyLexerOpBuiltin
"""
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpBuiltin,
    CrupyLexerOpBuiltinException,
)

#---
# Public
#---

def test_any() -> None:
    """ test any builtin
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('any'),
    })
    parser.register_stream('a\\"\\\\ \a')
    node0 = parser.execute('entry')
    node1 = parser.execute('entry')
    node2 = parser.execute('entry')
    node3 = parser.execute('entry')
    assert node0.type == 'lex_text'
    assert node0.text == 'a'
    assert node1.type == 'lex_text'
    assert node1.text == '"'
    assert node2.type == 'lex_text'
    assert node2.text == '\\'
    assert node3.type == 'lex_text'
    assert node3.text == ' '
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 7\n'
            'a\\"\\\\ \a\n'
            '      ^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "any"'
        )

def test_alphanum() -> None:
    """ simple valid cases
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('alphanum'),
    })
    parser.register_stream('aZ667-')
    strop0 = parser.execute('entry')
    strop1 = parser.execute('entry')
    strop2 = parser.execute('entry')
    strop3 = parser.execute('entry')
    strop4 = parser.execute('entry')
    assert strop0.type == 'lex_text'
    assert strop1.type == 'lex_text'
    assert strop0.text == 'a'
    assert strop1.text == 'Z'
    assert strop2.text == '6'
    assert strop3.text == '6'
    assert strop4.text == '7'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 6\n'
            'aZ667-\n'
            '     ^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "alphanum"'
        )

def test_alphanum_lower() -> None:
    """ simple valid cases
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('alphanum_lower'),
    })
    parser.register_stream('a667Z')
    strop0 = parser.execute('entry')
    strop1 = parser.execute('entry')
    strop2 = parser.execute('entry')
    strop3 = parser.execute('entry')
    assert strop0.type == 'lex_text'
    assert strop1.type == 'lex_text'
    assert strop0.text == 'a'
    assert strop1.text == '6'
    assert strop2.text == '6'
    assert strop3.text == '7'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 5\n'
            'a667Z\n'
            '    ^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "alphanum_lower"'
        )

def test_alphanum_upper() -> None:
    """ simple valid cases
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('alphanum_upper'),
    })
    parser.register_stream('A667z')
    strop0 = parser.execute('entry')
    strop1 = parser.execute('entry')
    strop2 = parser.execute('entry')
    strop3 = parser.execute('entry')
    assert strop0.type == 'lex_text'
    assert strop1.type == 'lex_text'
    assert strop0.text == 'A'
    assert strop1.text == '6'
    assert strop2.text == '6'
    assert strop3.text == '7'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 5\n'
            'A667z\n'
            '    ^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "alphanum_upper"'
        )

def test_alpha() -> None:
    """ simple valid cases
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('alpha'),
    })
    parser.register_stream('aZ1')
    strop0 = parser.execute('entry')
    strop1 = parser.execute('entry')
    assert strop0.type == 'lex_text'
    assert strop1.type == 'lex_text'
    assert strop0.text == 'a'
    assert strop1.text == 'Z'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 3\n'
            'aZ1\n'
            '  ^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "alpha"'
        )

def test_alpha_lower() -> None:
    """ simple valid cases
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('alpha_lower'),
    })
    parser.register_stream('azZ')
    strop0 = parser.execute('entry')
    strop1 = parser.execute('entry')
    assert strop0.type == 'lex_text'
    assert strop1.type == 'lex_text'
    assert strop0.text == 'a'
    assert strop1.text == 'z'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 3\n'
            'azZ\n'
            '  ^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "alpha_lower"'
        )

def test_alpha_upper() -> None:
    """ simple valid cases
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('alpha_upper'),
    })
    parser.register_stream('AZw')
    strop0 = parser.execute('entry')
    strop1 = parser.execute('entry')
    assert strop0.type == 'lex_text'
    assert strop1.type == 'lex_text'
    assert strop0.text == 'A'
    assert strop1.text == 'Z'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 3\n'
            'AZw\n'
            '  ^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "alpha_upper"'
        )

def test_digit() -> None:
    """ simple valid cases
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('digit'),
    })
    parser.register_stream('09A')
    strop0 = parser.execute('entry')
    strop1 = parser.execute('entry')
    assert strop0.type == 'lex_text'
    assert strop1.type == 'lex_text'
    assert strop0.text == '0'
    assert strop1.text == '9'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 3\n'
            '09A\n'
            '  ^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "digit"'
        )

def test_number() -> None:
    """ simple valid cases
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('number'),
    })
    parser.register_stream('667,')
    strop0 = parser.execute('entry')
    assert strop0.type == 'lex_text'
    assert strop0.text == '667'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 4\n'
            '667,\n'
            '   ^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "number"'
        )

def test_symbol() -> None:
    """ simple valid cases
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('symbol'),
    })
    parser.register_stream('{*\\t')
    strop0 = parser.execute('entry')
    strop1 = parser.execute('entry')
    strop2 = parser.execute('entry')
    assert strop0.type == 'lex_text'
    assert strop1.type == 'lex_text'
    assert strop0.text == '{'
    assert strop1.text == '*'
    assert strop2.text == '\\'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 4\n'
            '{*\\t\n'
            '   ^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "symbol"'
        )

def test_space() -> None:
    """ test space
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('space'),
    })
    parser.register_stream(' \tabc')
    assert parser.execute('entry') is not None
    assert parser.execute('entry') is not None
    with parser.stream as context:
        assert context.read_char() == 'a'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 3\n'
            ' \tabc\n'
            '        ^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "space"'
        )

def test_space_nl() -> None:
    """ test space
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('space_nl'),
        'test0' : CrupyLexerOpBuiltin('any'),
    })
    parser.register_stream(' \t\nabc')
    assert parser.execute('entry') is not None
    assert parser.execute('entry') is not None
    assert parser.execute('entry') is not None
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 2, column 1\n'
            'abc\n'
            '^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "space_nl"'
        )

def test_eof() -> None:
    """ test space
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpBuiltin('eof'),
    })
    parser.register_stream('a')
    with parser.stream as context:
        context.read_char()
        assert parser.execute('entry') is not None
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 1\n'
            'a\n'
            '^\n'
            'CrupyLexerOpBuiltinException: Unable to validate the '
            'current char as "EOF", stream available'
        )
