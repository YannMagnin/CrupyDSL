"""
tests.lexer.op_text     - test the CrupyLexerOpText
"""
from crupydsl.parser import CrupyParserBase
from crupydsl.parser._lexer import (
    CrupyLexerOpText,
    CrupyLexerOpTextException,
)

#---
# Public
#---

def test_simple_success() -> None:
    """ simple valid cases
    """
    parser = CrupyParserBase({
        'entry0' : CrupyLexerOpText('abcdef'),
        'entry1' : CrupyLexerOpText('i'),
        'entry3' : CrupyLexerOpText('jkl'),
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
    parser = CrupyParserBase({
        'entry0' : CrupyLexerOpText('abcdef'),
        'entry1' : CrupyLexerOpText('jkl'),
    })
    parser.register_stream('abcdefijkl')
    assert parser.execute('entry0') is not None
    try:
        parser.execute('entry1')
        raise AssertionError('production entry1 has been executed')
    except CrupyLexerOpTextException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 7\n'
            'abcdefijkl\n'
            '      ^\n'
            'CrupyLexerOpTextException: Unable to match the text '
            '\'jkl\''
        )
        assert err.read == 0
        assert err.match == 'jkl'
        assert err.reason == 'unable to match the text \'jkl\''

def test_eof_error() -> None:
    """ test EOF handling
    """
    parser = CrupyParserBase({
        'entry0' : CrupyLexerOpText('abcdef'),
        'entry1' : CrupyLexerOpText('ijklm'),
    })
    parser.register_stream('abcdefijkl')
    assert parser.execute('entry0') is not None
    try:
        parser.execute('entry1')
        raise AssertionError('production entry1 has been executed')
    except CrupyLexerOpTextException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 11\n'
            'abcdefijkl\n'
            '      ~~~~^\n'
            'CrupyLexerOpTextException: Reached end-of-file'
        )
