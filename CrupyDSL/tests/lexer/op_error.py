"""
tests.lexer.op_error    - test the CrupyDSLLexerOpError
"""
from crupydsl.parser import (
    CrupyDSLParserBase,
    CrupyDSLParserBaseException,
)
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpError,
    CrupyDSLLexerOpSeq,
    CrupyDSLLexerOpOr,
    CrupyDSLLexerOpOptional,
)

#---
# Public
#---

def test_simple() -> None:
    """ simple valid case
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpError('foo bar ekip'),
    })
    try:
        parser.register_stream('aaaaaaaa')
        parser.execute('entry')
        assert AssertionError('production entry has been executed')
    except CrupyDSLParserBaseException as err:
        assert err.reason == 'foo bar ekip'

def test_in_seq() -> None:
    """ simple valid case
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpError('foo bar ekip'),
        ),
    })
    try:
        parser.register_stream('aaaaaaaa')
        parser.execute('entry')
        raise AssertionError('production entry has been executed')
    except CrupyDSLParserBaseException as err:
        assert err.reason == 'foo bar ekip'

def test_in_or() -> None:
    """ simple valid case
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpOr(
            CrupyDSLLexerOpError('foo bar ekip'),
        ),
    })
    try:
        parser.register_stream('aaaaaaaa')
        parser.execute('entry')
        raise AssertionError('production entry has been executed')
    except CrupyDSLParserBaseException as err:
        assert err.reason == 'foo bar ekip'

def test_in_optional() -> None:
    """ simple valid case
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpOptional(
            CrupyDSLLexerOpError('foo bar ekip'),
        ),
    })
    try:
        parser.register_stream('aaaaaaaa')
        parser.execute('entry')
    except CrupyDSLParserBaseException as err:
        raise AssertionError(
            'production entry has raised exception'
        ) from err

def test_in_seq_and_or() -> None:
    """ simple valid case
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpOr(
                CrupyDSLLexerOpError('foo bar ekip'),
            ),
        ),
    })
    try:
        parser.register_stream('aaaaaaaa')
        parser.execute('entry')
        raise AssertionError('production entry has been executed')
    except CrupyDSLParserBaseException as err:
        assert err.reason == 'foo bar ekip'
