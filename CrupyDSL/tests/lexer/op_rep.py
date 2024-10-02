"""
tests.lexer.op_rep  - tes for the CrupyDSLLexerOpRep0N, and CrupyDSLLexerOpRep1N
"""
from crupydsl.parser import CrupyDSLParserBase
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpRep0N,
    CrupyDSLLexerOpRep1N,
    CrupyDSLLexerException,
)

#---
# Public
#---

## Rep0N

def test_rep0n_simple_success() -> None:
    """ simple valid case
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpRep0N(
            CrupyDSLLexerOpText('abc'),
            CrupyDSLLexerOpText('def'),
            CrupyDSLLexerOpText('ij'),
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
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpRep0N(
            CrupyDSLLexerOpText('zzz'),
            CrupyDSLLexerOpText('def'),
            CrupyDSLLexerOpText('ijk'),
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
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpRep1N(
            CrupyDSLLexerOpText('abc'),
            CrupyDSLLexerOpText('def'),
            CrupyDSLLexerOpText('ij'),
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
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpRep1N(
            CrupyDSLLexerOpText('abc'),
            CrupyDSLLexerOpText('def'),
            CrupyDSLLexerOpText('ijk'),
        ),
    })
    try:
        parser.register_stream('abcdefijabcdefijklnm')
        parser.execute('entry')
        raise AssertionError('rule entry executed')
    except CrupyDSLLexerException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 9\n'
            'abcdefijabcdefijklnm\n'
            '      ~~^\n'
            'CrupyDSLLexerOpTextException: Unable to match the text \'ijk\''
        )
        assert err.reason == 'unable to match the text \'ijk\''
