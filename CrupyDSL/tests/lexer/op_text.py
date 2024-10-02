"""
tests.lexer.op_text     - test the CrupyDSLLexerOpText
"""
from crupydsl.parser import CrupyDSLParserBase
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpTextException,
)

#---
# Public
#---

def test_simple_success() -> None:
    """ simple valid cases
    """
    parser = CrupyDSLParserBase({
        'entry0' : CrupyDSLLexerOpText('abcdef'),
        'entry1' : CrupyDSLLexerOpText('i'),
        'entry3' : CrupyDSLLexerOpText('jkl'),
    })
    parser.register_stream('abcdefijkl')
    strop0 = parser.execute('entry0')
    strop1 = parser.execute('entry1')
    strop3 = parser.execute('entry3')
    assert strop0 is not None
    assert strop1 is not None
    assert strop3 is not None

def test_simple_error() -> None:
    """ simple error case
    """
    parser = CrupyDSLParserBase({
        'entry0' : CrupyDSLLexerOpText('abcdef'),
        'entry1' : CrupyDSLLexerOpText('jkl'),
    })
    parser.register_stream('abcdefijkl')
    assert parser.execute('entry0') is not None
    try:
        parser.execute('entry1')
        raise AssertionError('production entry1 has been executed')
    except CrupyDSLLexerOpTextException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 7\n'
            'abcdefijkl\n'
            '      ^\n'
            'CrupyDSLLexerOpTextException: Unable to match the text '
            '\'jkl\''
        )
        assert err.read == 0
        assert err.match == 'jkl'
        assert err.reason == 'unable to match the text \'jkl\''

def test_eof_error() -> None:
    """ test EOF handling
    """
    parser = CrupyDSLParserBase({
        'entry0' : CrupyDSLLexerOpText('abcdef'),
        'entry1' : CrupyDSLLexerOpText('ijklm'),
    })
    parser.register_stream('abcdefijkl')
    assert parser.execute('entry0') is not None
    try:
        parser.execute('entry1')
        raise AssertionError('production entry1 has been executed')
    except CrupyDSLLexerOpTextException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 11\n'
            'abcdefijkl\n'
            '      ~~~~^\n'
            'CrupyDSLLexerOpTextException: Reached end-of-file'
        )
