"""
tests.lexer.op_production   - test the CrupyLexerOpProduction
"""
from crupydsl.parser import CrupyParserBase
from crupydsl.parser._lexer import (
    CrupyLexerOpProductionCall,
    CrupyLexerOpText,
    CrupyLexerOpProductionCallException,
)

#---
# Public
#---

def test_simple_success() -> None:
    """ simple success test
    """
    parser = CrupyParserBase({
        'entry'  : CrupyLexerOpProductionCall('entry2'),
        'entry2' : CrupyLexerOpText('abcdef')
    })
    parser.register_stream('abcdefijkl')
    test = parser.execute('entry')
    assert test.text == 'abcdef'
    with parser.stream as context:
        for n in 'ijkl':
            assert context.read_char() == n

def test_raise_error() -> None:
    """ force production calling that not exists
    """
    parser = CrupyParserBase({
        'entry'  : CrupyLexerOpProductionCall('entry2'),
    })
    parser.register_stream('abcdefijkl')
    try:
        parser.execute('entry')
        raise AssertionError('production entry has been executed')
    except CrupyLexerOpProductionCallException as err:
        assert err.production == 'entry2'
        assert err.reason == (
            'unable to find the production named \'entry2\''
        )
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 1\n'
            'abcdefijkl\n'
            '^\n'
            'CrupyLexerOpProductionCallException: Unable to find the '
            'production named \'entry2\''
        )
