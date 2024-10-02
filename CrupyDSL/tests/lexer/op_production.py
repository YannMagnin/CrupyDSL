"""
tests.lexer.op_production   - test the CrupyDSLLexerOpProduction
"""
from crupydsl.parser import CrupyDSLParserBase
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpProductionCall,
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpProductionCallException,
)

#---
# Public
#---

def test_simple_success() -> None:
    """ simple success test
    """
    parser = CrupyDSLParserBase({
        'entry'  : CrupyDSLLexerOpProductionCall('entry2'),
        'entry2' : CrupyDSLLexerOpText('abcdef')
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
    parser = CrupyDSLParserBase({
        'entry'  : CrupyDSLLexerOpProductionCall('entry2'),
    })
    parser.register_stream('abcdefijkl')
    try:
        parser.execute('entry')
        raise AssertionError('production entry has been executed')
    except CrupyDSLLexerOpProductionCallException as err:
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
            'CrupyDSLLexerOpProductionCallException: Unable to find the '
            'production named \'entry2\''
        )
