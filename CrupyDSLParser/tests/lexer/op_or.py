"""
tests.lexer.op_or   - test the CrupyLexerOpOr
"""
from crupydslparser.parser import (
    CrupyParserBase,
    CrupyParserBaseException,
)
from crupydslparser.parser._lexer import (
    CrupyLexerOpOr,
    CrupyLexerOpOrException,
    CrupyLexerOpText,
    CrupyLexerOpError,
    CrupyLexerOpSeq,
)

#---
# Public
#---

def test_simple_success0() -> None:
    """ simple valid case
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpOr(
            CrupyLexerOpText('abc'),
            CrupyLexerOpText('abcdef'),
        ),
    })
    parser.register_stream('abcdefijkl')
    or_op = parser.execute('entry')
    assert or_op.text == 'abc'
    with parser.stream as context:
        for n in 'defijkl':
            assert context.read_char() == n

def test_simple_success1() -> None:
    """ simple valid case
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpOr(
            CrupyLexerOpText('zzz'),
            CrupyLexerOpText('zzz'),
            CrupyLexerOpText('zzz'),
            CrupyLexerOpText('zzz'),
            CrupyLexerOpText('abcdef'),
        ),
    })
    parser.register_stream('abcdefijkl')
    or_op = parser.execute('entry')
    assert or_op.text == 'abcdef'
    with parser.stream as context:
        for n in 'ijkl':
            assert context.read_char() == n

def test_error() -> None:
    """ depth error handling test
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpOr(
            CrupyLexerOpText('ax'),
            CrupyLexerOpText('abcdef'),
            CrupyLexerOpText('abcx'),
            CrupyLexerOpText('xx'),
            CrupyLexerOpText('ekip'),
        ),
    })
    parser.register_stream('abcdexxx')
    try:
        parser.execute('entry')
        raise AssertionError('production entry has been executed')
    except CrupyLexerOpOrException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 6\n'
            'abcdexxx\n'
            '~~~~~^\n'
            'CrupyLexerOpTextException: Unable to match the '
            'text \'abcdef\''
        )
        assert err.deepest_error is not None
        assert err.reason == 'unable to match the text \'abcdef\''

def test_error_and_success() -> None:
    """ handle error operation
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpOr(
            CrupyLexerOpError('test'),
            CrupyLexerOpError('test'),
            CrupyLexerOpError('test'),
            CrupyLexerOpError('test'),
            CrupyLexerOpText('ax'),
            CrupyLexerOpText('abcdef'),
            CrupyLexerOpText('abcx'),
            CrupyLexerOpText('xx'),
            CrupyLexerOpText('ekip'),
        ),
    })
    parser.register_stream('ekip')
    parser.execute('entry')

def test_multiple_error() -> None:
    """ handle error operation
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpOr(
            CrupyLexerOpSeq(
                CrupyLexerOpText('e'),
                CrupyLexerOpError('fail1'),
            ),
            CrupyLexerOpSeq(
                CrupyLexerOpText('ekip'),
                CrupyLexerOpError('success'),
            ),
            CrupyLexerOpSeq(
                CrupyLexerOpText('eki'),
                CrupyLexerOpError('fail2'),
            ),
        ),
    })
    try:
        parser.register_stream('ekip')
        parser.execute('entry')
        raise AssertionError('entry has been executed')
    except CrupyParserBaseException:
        pass

def test_manual_error() -> None:
    """ test
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpOr(
            CrupyLexerOpError('salut a tous'),
        ),
    })
    try:
        parser.register_stream('gang')
        parser.execute('entry')
        raise AssertionError('entry has been executed')
    except CrupyParserBaseException as err:
        assert err.reason == 'salut a tous'
