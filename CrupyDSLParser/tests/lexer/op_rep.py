"""
tests.lexer.op_rep  - tes for the CrupyLexerOpRep0N, and CrupyLexerOpRep1N
"""
from crupydslparser.parser import CrupyParserBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpText,
    CrupyLexerOpRep0N,
    CrupyLexerOpRep1N,
    CrupyLexerException,
)

#---
# Public
#---

## Rep0N

def test_rep0n_simple_success() -> None:
    """ simple valid case
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpRep0N(
            CrupyLexerOpText('abc'),
            CrupyLexerOpText('def'),
            CrupyLexerOpText('ij'),
        ),
    })
    parser.register_stream('abcdefijabcdefijklnm')
    reptok = parser.execute('entry')
    assert reptok.rep is not None
    assert len(reptok.rep) == 2
    assert len(reptok.rep[0]) == 3
    assert reptok.rep[0][0].text == 'abc'
    assert reptok.rep[0][1].text == 'def'
    assert reptok.rep[0][2].text == 'ij'
    assert reptok.rep[1][0].text == 'abc'
    assert reptok.rep[1][1].text == 'def'
    assert reptok.rep[1][2].text == 'ij'

def test_rep0n_empty() -> None:
    """ simple empty
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpRep0N(
            CrupyLexerOpText('zzz'),
            CrupyLexerOpText('def'),
            CrupyLexerOpText('ijk'),
        ),
    })
    parser.register_stream('abcdefijabcdefijklnm')
    reptok = parser.execute('entry')
    assert reptok.rep is not None
    assert len(reptok.rep) == 0

## Rep1N

def test_rep1n_simple_success() -> None:
    """ simple valid case
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpRep1N(
            CrupyLexerOpText('abc'),
            CrupyLexerOpText('def'),
            CrupyLexerOpText('ij'),
        ),
    })
    parser.register_stream('abcdefij')
    reptok = parser.execute('entry')
    assert reptok.rep is not None
    assert len(reptok.rep) == 1
    assert len(reptok.rep[0]) == 3
    assert reptok.rep[0][0].text == 'abc'
    assert reptok.rep[0][1].text == 'def'
    assert reptok.rep[0][2].text == 'ij'

def test_rep1n_empty() -> None:
    """ simple empty
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpRep1N(
            CrupyLexerOpText('abc'),
            CrupyLexerOpText('def'),
            CrupyLexerOpText('ijk'),
        ),
    })
    try:
        parser.register_stream('abcdefijabcdefijklnm')
        parser.execute('entry')
        raise AssertionError('rule entry executed')
    except CrupyLexerException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 9\n'
            'abcdefijabcdefijklnm\n'
            '      ~~^\n'
            'CrupyLexerOpTextException: Unable to match the text \'ijk\''
        )
        assert err.reason == 'unable to match the text \'ijk\''
