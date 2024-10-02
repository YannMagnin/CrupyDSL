"""
tests.lexer.op_builtin      - test the CrupyDSLLexerOpBuiltin
"""
from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpBuiltin,
    CrupyDSLLexerOpBuiltinException,
)

#---
# Public
#---

def test_any() -> None:
    """ test any builtin
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('any'),
    })
    parser.register_stream(r'a\"\\ ' + '\r\n')
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
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 7\n'
           r'a\"\\ \r\n' + '\n'
            '      ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "any"'
        )

def test_any_newline() -> None:
    """ test any builtin
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('any_newline'),
    })
    parser.register_stream('a\\"\\\\ \n\r\nk')
    node0 = parser.execute('entry')
    node1 = parser.execute('entry')
    node2 = parser.execute('entry')
    node3 = parser.execute('entry')
    node4 = parser.execute('entry')
    node5 = parser.execute('entry')
    node6 = parser.execute('entry')
    assert node0.type == 'lex_text'
    assert node0.text == 'a'
    assert node1.type == 'lex_text'
    assert node1.text == '"'
    assert node2.type == 'lex_text'
    assert node2.text == '\\'
    assert node3.type == 'lex_text'
    assert node3.text == ' '
    assert node4.type == 'lex_text'
    assert node4.text == '\n'
    assert node5.type == 'lex_text'
    assert node5.text == '\r\n'
    assert node6.type == 'lex_text'
    assert node6.text == 'k'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 3, column 2\n'
            'k\n'
            ' ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "any_newline"'
        )

def test_alphanum() -> None:
    """ simple valid cases
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('alphanum'),
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
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 6\n'
            'aZ667-\n'
            '     ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "alphanum"'
        )

def test_alphanum_lower() -> None:
    """ simple valid cases
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('alphanum_lower'),
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
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 5\n'
            'a667Z\n'
            '    ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "alphanum_lower"'
        )

def test_alphanum_upper() -> None:
    """ simple valid cases
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('alphanum_upper'),
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
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 5\n'
            'A667z\n'
            '    ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "alphanum_upper"'
        )

def test_alpha() -> None:
    """ simple valid cases
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('alpha'),
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
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 3\n'
            'aZ1\n'
            '  ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "alpha"'
        )

def test_alpha_lower() -> None:
    """ simple valid cases
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('alpha_lower'),
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
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 3\n'
            'azZ\n'
            '  ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "alpha_lower"'
        )

def test_alpha_upper() -> None:
    """ simple valid cases
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('alpha_upper'),
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
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 3\n'
            'AZw\n'
            '  ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "alpha_upper"'
        )

def test_digit() -> None:
    """ simple valid cases
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('digit'),
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
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 3\n'
            '09A\n'
            '  ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "digit"'
        )

def test_number() -> None:
    """ simple valid cases
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('number'),
    })
    parser.register_stream('667,')
    strop0 = parser.execute('entry')
    assert strop0.type == 'lex_text'
    assert strop0.text == '667'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 4\n'
            '667,\n'
            '   ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "number"'
        )

def test_newline() -> None:
    """ simple tests
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('newline'),
        'test0' : CrupyDSLLexerOpBuiltin('any'),
    })
    parser.register_stream('\n\r\n\ra')
    strop0 = parser.execute('entry')
    strop1 = parser.execute('entry')
    assert strop0.type == 'lex_text'
    assert strop0.text == '\n'
    assert strop1.type == 'lex_text'
    assert strop1.text == '\r\n'
    try:
        parser.execute('entry')
        raise AssertionError('production executed 0')
    except CrupyDSLLexerOpBuiltinException as err:
        assert err.reason == (
            'unable to validate the current char as "newline"'
        )
    assert parser.execute('test0').text == '\r'
    assert parser.execute('test0').text == 'a'
    try:
        parser.execute('entry')
        raise AssertionError('production executed 1')
    except CrupyDSLLexerOpBuiltinException as err:
        assert err.reason == (
            'unable to validate the current char as "newline", '
            'no stream available'
        )

def test_symbol() -> None:
    """ simple valid cases
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('symbol'),
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
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 4\n'
            '{*\\t\n'
            '   ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "symbol"'
        )

def test_space() -> None:
    """ test space
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('space'),
    })
    parser.register_stream(' \tabc')
    node0 = parser.execute('entry')
    node1 = parser.execute('entry')
    assert node0.type == 'lex_text'
    assert node0.text == ' '
    assert node1.type == 'lex_text'
    assert node1.text == '\t'
    with parser.stream as context:
        assert context.read_char() == 'a'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 3\n'
            '    abc\n'
            '    ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "space"'
        )

def test_space_newline() -> None:
    """ test space
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('space_newline'),
        'test0' : CrupyDSLLexerOpBuiltin('any'),
    })
    parser.register_stream(' \t\n\r\nabc')
    node0 = parser.execute('entry')
    node1 = parser.execute('entry')
    node2 = parser.execute('entry')
    node3 = parser.execute('entry')
    assert node0.type == 'lex_text'
    assert node0.text == ' '
    assert node1.type == 'lex_text'
    assert node1.text == '\t'
    assert node2.type == 'lex_text'
    assert node2.text == '\n'
    assert node3.type == 'lex_text'
    assert node3.text == '\r\n'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 3, column 1\n'
            'abc\n'
            '^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "space_newline"'
        )

def test_spaces() -> None:
    """ test spaces
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('spaces'),
    })
    parser.register_stream(' \tabc')
    node0 = parser.execute('entry')
    assert node0.type == 'lex_text'
    assert node0.text == ' \t'
    with parser.stream as context:
        assert context.read_char() == 'a'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 3\n'
            '    abc\n'
            '    ^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "spaces"'
        )

def test_spaces_newline() -> None:
    """ test spaces
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('spaces_newline'),
        'test0' : CrupyDSLLexerOpBuiltin('any'),
    })
    parser.register_stream(' \t\n\r\nabc')
    node0 = parser.execute('entry')
    assert node0.type == 'lex_text'
    assert node0.text == ' \t\n\r\n'
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 3, column 1\n'
            'abc\n'
            '^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "spaces_newline"'
        )

def test_eof() -> None:
    """ test space
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpBuiltin('eof'),
    })
    parser.register_stream('a')
    with parser.stream as context:
        context.read_char()
        assert parser.execute('entry') is not None
    try:
        parser.execute('entry')
        raise AssertionError('No lexer exception has occured')
    except CrupyDSLLexerOpBuiltinException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 1\n'
            'a\n'
            '^\n'
            'CrupyDSLLexerOpBuiltinException: Unable to validate the '
            'current char as "EOF", stream available'
        )
