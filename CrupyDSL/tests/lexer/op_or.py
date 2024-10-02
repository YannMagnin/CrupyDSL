"""
tests.lexer.op_or   - test the CrupyDSLLexerOpOr
"""
from crupydsl.parser import (
    CrupyDSLParserBase,
    CrupyDSLParserBaseException,
)
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpOr,
    CrupyDSLLexerOpOrException,
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpError,
    CrupyDSLLexerOpSeq,
)

#---
# Public
#---

def test_simple_success0() -> None:
    """ simple valid case
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpOr(
            CrupyDSLLexerOpText('abc'),
            CrupyDSLLexerOpText('abcdef'),
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
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpOr(
            CrupyDSLLexerOpText('zzz'),
            CrupyDSLLexerOpText('zzz'),
            CrupyDSLLexerOpText('zzz'),
            CrupyDSLLexerOpText('zzz'),
            CrupyDSLLexerOpText('abcdef'),
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
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpOr(
            CrupyDSLLexerOpText('ax'),
            CrupyDSLLexerOpText('abcdef'),
            CrupyDSLLexerOpText('abcx'),
            CrupyDSLLexerOpText('xx'),
            CrupyDSLLexerOpText('ekip'),
        ),
    })
    parser.register_stream('abcdexxx')
    try:
        parser.execute('entry')
        raise AssertionError('production entry has been executed')
    except CrupyDSLLexerOpOrException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 6\n'
            'abcdexxx\n'
            '~~~~~^\n'
            'CrupyDSLLexerOpTextException: Unable to match the '
            'text \'abcdef\''
        )
        assert err.deepest_error is not None
        assert err.reason == 'unable to match the text \'abcdef\''

def test_error_and_success() -> None:
    """ handle error operation
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpOr(
            CrupyDSLLexerOpError('test'),
            CrupyDSLLexerOpError('test'),
            CrupyDSLLexerOpError('test'),
            CrupyDSLLexerOpError('test'),
            CrupyDSLLexerOpText('ax'),
            CrupyDSLLexerOpText('abcdef'),
            CrupyDSLLexerOpText('abcx'),
            CrupyDSLLexerOpText('xx'),
            CrupyDSLLexerOpText('ekip'),
        ),
    })
    parser.register_stream('ekip')
    parser.execute('entry')

def test_multiple_error() -> None:
    """ handle error operation
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpOr(
            CrupyDSLLexerOpSeq(
                CrupyDSLLexerOpText('e'),
                CrupyDSLLexerOpError('fail1'),
            ),
            CrupyDSLLexerOpSeq(
                CrupyDSLLexerOpText('ekip'),
                CrupyDSLLexerOpError('success'),
            ),
            CrupyDSLLexerOpSeq(
                CrupyDSLLexerOpText('eki'),
                CrupyDSLLexerOpError('fail2'),
            ),
        ),
    })
    try:
        parser.register_stream('ekip')
        parser.execute('entry')
        raise AssertionError('entry has been executed')
    except CrupyDSLParserBaseException:
        pass

def test_manual_error() -> None:
    """ test
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpOr(
            CrupyDSLLexerOpError('salut a tous'),
        ),
    })
    try:
        parser.register_stream('gang')
        parser.execute('entry')
        raise AssertionError('entry has been executed')
    except CrupyDSLParserBaseException as err:
        assert err.reason == 'salut a tous'
