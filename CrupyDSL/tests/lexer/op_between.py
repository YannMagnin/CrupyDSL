"""
tests.lexer.op_between      - test the CrupyLexerOpBetween
"""
from crupydsl.parser import CrupyParserBase
from crupydsl.parser._lexer import (
    CrupyLexerOpText,
    CrupyLexerOpSeq,
    CrupyLexerOpBetween,
    CrupyLexerOpBetweenException,
)

#---
# Public
#---

## valid whithout newline

def test_nonl_success_0() -> None:
    """ valid test """
    parser = CrupyParserBase({
        'entry' : \
            CrupyLexerOpBetween(
                startop         = CrupyLexerOpText('"'),
                endop           = CrupyLexerOpText('"'),
                with_newline    = False,
            ),
    })
    parser.register_stream('"this is a test yes no"')
    node = parser.execute('entry')
    assert node.type == 'lex_between'
    assert node.captured_start.type == 'lex_text'
    assert node.captured_start.text == '"'
    assert node.captured_middle == 'this is a test yes no'
    assert node.captured_end.type == 'lex_text'
    assert node.captured_end.text == '"'

def test_nonl_success_1() -> None:
    """ valid test """
    parser = CrupyParserBase({
        'entry' : \
            CrupyLexerOpBetween(
                startop         = CrupyLexerOpText('"'),
                endop           = \
                    CrupyLexerOpSeq(
                        CrupyLexerOpText('a'),
                        CrupyLexerOpText('b'),
                    ),
                with_newline    = False,
            ),
    })
    parser.register_stream('"this is a test no aaaab"')
    node = parser.execute('entry')
    assert node.type == 'lex_between'
    assert node.captured_start.type == 'lex_text'
    assert node.captured_start.text == '"'
    assert node.captured_middle == 'this is a test no aaa'
    assert node.captured_end.type == 'lex_seq'
    assert len(node.captured_end.seq) == 2
    assert node.captured_end.seq[0].type == 'lex_text'
    assert node.captured_end.seq[0].text == 'a'
    assert node.captured_end.seq[1].type == 'lex_text'
    assert node.captured_end.seq[1].text == 'b'

def test_nonl_success_2() -> None:
    """ valid test """
    parser = CrupyParserBase({
        'entry' : \
            CrupyLexerOpBetween(
                startop         = \
                    CrupyLexerOpSeq(
                        CrupyLexerOpText('a'),
                        CrupyLexerOpText('b'),
                    ),
                endop           = CrupyLexerOpText('"'),
                with_newline    = False,
            ),
    })
    parser.register_stream('abthis is a test no"')
    node = parser.execute('entry')
    assert node.type == 'lex_between'
    assert node.captured_start.type == 'lex_seq'
    assert len(node.captured_start.seq) == 2
    assert node.captured_start.seq[0].type == 'lex_text'
    assert node.captured_start.seq[0].text == 'a'
    assert node.captured_start.seq[1].type == 'lex_text'
    assert node.captured_start.seq[1].text == 'b'
    assert node.captured_middle == 'this is a test no'
    assert node.captured_end.type == 'lex_text'
    assert node.captured_end.text == '"'

## valid whithout newline

def test_nl_success_0() -> None:
    """ valid test """
    parser = CrupyParserBase({
        'entry' : \
            CrupyLexerOpBetween(
                startop         = CrupyLexerOpText('"'),
                endop           = CrupyLexerOpText('"'),
                with_newline    = True,
            ),
    })
    parser.register_stream('"this is a \ntest\r\nyes no"')
    node = parser.execute('entry')
    assert node.type == 'lex_between'
    assert node.captured_start.type == 'lex_text'
    assert node.captured_start.text == '"'
    assert node.captured_middle == 'this is a \ntest\r\nyes no'
    assert node.captured_end.type == 'lex_text'
    assert node.captured_end.text == '"'

def test_nl_success_1() -> None:
    """ valid test """
    parser = CrupyParserBase({
        'entry' : \
            CrupyLexerOpBetween(
                startop         = CrupyLexerOpText('"'),
                endop           = \
                    CrupyLexerOpSeq(
                        CrupyLexerOpText('a'),
                        CrupyLexerOpText('b'),
                    ),
                with_newline    = True,
            ),
    })
    parser.register_stream('"this is a test no\r\n\naaaab"')
    node = parser.execute('entry')
    assert node.type == 'lex_between'
    assert node.captured_start.type == 'lex_text'
    assert node.captured_start.text == '"'
    assert node.captured_middle == 'this is a test no\r\n\naaa'
    assert node.captured_end.type == 'lex_seq'
    assert len(node.captured_end.seq) == 2
    assert node.captured_end.seq[0].type == 'lex_text'
    assert node.captured_end.seq[0].text == 'a'
    assert node.captured_end.seq[1].type == 'lex_text'
    assert node.captured_end.seq[1].text == 'b'

def test_nl_success_2() -> None:
    """ valid test """
    parser = CrupyParserBase({
        'entry' : \
            CrupyLexerOpBetween(
                startop         = \
                    CrupyLexerOpSeq(
                        CrupyLexerOpText('a'),
                        CrupyLexerOpText('b'),
                    ),
                endop           = CrupyLexerOpText('"'),
                with_newline    = True,
            ),
    })
    parser.register_stream('abthis \nis \r\na test no\n"')
    node = parser.execute('entry')
    assert node.type == 'lex_between'
    assert node.captured_start.type == 'lex_seq'
    assert len(node.captured_start.seq) == 2
    assert node.captured_start.seq[0].type == 'lex_text'
    assert node.captured_start.seq[0].text == 'a'
    assert node.captured_start.seq[1].type == 'lex_text'
    assert node.captured_start.seq[1].text == 'b'
    assert node.captured_middle == 'this \nis \r\na test no\n'
    assert node.captured_end.type == 'lex_text'
    assert node.captured_end.text == '"'

## error - no newline

def test_nonl_fail_0() -> None:
    """ fail test """
    parser = CrupyParserBase({
        'entry' : \
            CrupyLexerOpBetween(
                startop         = CrupyLexerOpText('"'),
                endop           = CrupyLexerOpText('"'),
                with_newline    = True,
            ),
    })
    parser.register_stream('zthis is a test yes no"')
    try:
        parser.execute('entry')
        raise AssertionError('production executed')
    except CrupyLexerOpBetweenException as err:
        assert err.reason == (
            'unable to validate the opening request: '
            'unable to match the text \'"\''
        )
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 1\n'
            'zthis is a test yes no"\n'
            '^\n'
            'CrupyLexerOpBetweenException: Unable to validate the '
            'opening request: unable to match the text \'"\''
        )

def test_nonl_fail_1() -> None:
    """ fail test """
    parser = CrupyParserBase({
        'entry' : \
            CrupyLexerOpBetween(
                startop         = CrupyLexerOpText('"'),
                endop           = CrupyLexerOpText('"'),
                with_newline    = False,
            ),
    })
    parser.register_stream('"this is a \r\ntest yes no"')
    try:
        parser.execute('entry')
        raise AssertionError('production executed')
    except CrupyLexerOpBetweenException as err:
        assert err.reason == (
            'unable to validate the middle request: '
            'unable to validate the current char as "any"'
        )
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 12\n'
            '"this is a \\r\\n\n'
            '~~~~~~~~~~~^\n'
            'CrupyLexerOpBetweenException: Unable to validate the '
            'middle request: unable to validate the current char as "any"'
        )

def test_nonl_fail_2() -> None:
    """ fail test """
    parser = CrupyParserBase({
        'entry' : \
            CrupyLexerOpBetween(
                startop         = CrupyLexerOpText('"'),
                endop           = CrupyLexerOpText('"'),
                with_newline    = True,
            ),
    })
    parser.register_stream('"this is a \r\ntest yes nooo')
    try:
        parser.execute('entry')
        raise AssertionError('production executed')
    except CrupyLexerOpBetweenException as err:
        assert err.reason == (
            'unable to validate the enclosing request: reached end-of-file'
        )
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 2, column 14\n'
            'test yes nooo\n'
            '~~~~~~~~~~~~~^\n'
            'CrupyLexerOpBetweenException: Unable to validate the '
            'enclosing request: reached end-of-file'
        )
