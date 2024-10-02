"""
tests.lexer.op_error    - test the CrupyLexerOpError
"""
from crupydsl.parser import (
    CrupyParserBase,
    CrupyParserBaseException,
)
from crupydsl.parser._lexer import (
    CrupyLexerOpError,
    CrupyLexerOpSeq,
    CrupyLexerOpOr,
    CrupyLexerOpOptional,
)

#---
# Public
#---

def test_simple() -> None:
    """ simple valid case
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpError('foo bar ekip'),
    })
    try:
        parser.register_stream('aaaaaaaa')
        parser.execute('entry')
        assert AssertionError('production entry has been executed')
    except CrupyParserBaseException as err:
        assert err.reason == 'foo bar ekip'

def test_in_seq() -> None:
    """ simple valid case
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpSeq(
            CrupyLexerOpError('foo bar ekip'),
        ),
    })
    try:
        parser.register_stream('aaaaaaaa')
        parser.execute('entry')
        raise AssertionError('production entry has been executed')
    except CrupyParserBaseException as err:
        assert err.reason == 'foo bar ekip'

def test_in_or() -> None:
    """ simple valid case
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpOr(
            CrupyLexerOpError('foo bar ekip'),
        ),
    })
    try:
        parser.register_stream('aaaaaaaa')
        parser.execute('entry')
        raise AssertionError('production entry has been executed')
    except CrupyParserBaseException as err:
        assert err.reason == 'foo bar ekip'

def test_in_optional() -> None:
    """ simple valid case
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpOptional(
            CrupyLexerOpError('foo bar ekip'),
        ),
    })
    try:
        parser.register_stream('aaaaaaaa')
        parser.execute('entry')
    except CrupyParserBaseException as err:
        raise AssertionError(
            'production entry has raised exception'
        ) from err

def test_in_seq_and_or() -> None:
    """ simple valid case
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpSeq(
            CrupyLexerOpOr(
                CrupyLexerOpError('foo bar ekip'),
            ),
        ),
    })
    try:
        parser.register_stream('aaaaaaaa')
        parser.execute('entry')
        raise AssertionError('production entry has been executed')
    except CrupyParserBaseException as err:
        assert err.reason == 'foo bar ekip'
