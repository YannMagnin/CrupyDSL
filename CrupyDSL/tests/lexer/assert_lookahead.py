"""
tests.lexer.assert_lookahead  - test for the CrupyLexerAssertLookahead*
"""
from crupydsl.parser.base import CrupyParserBase
from crupydsl.parser._lexer import (
    CrupyLexerOpSeq,
    CrupyLexerOpText,
    CrupyLexerAssertLookaheadNegative,
    CrupyLexerAssertLookaheadPositive,
)

#---
# Public
#---

## tests - Negative

def test_neg_simple_success() -> None:
    """ simple valid case
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpSeq(
            CrupyLexerOpText('abc'),
            CrupyLexerAssertLookaheadNegative(
                CrupyLexerOpText('d'),
                CrupyLexerOpText('r'),
                CrupyLexerOpText('x'),
            ),
        ),
    })
    parser.register_stream('abcdrabcde')
    node = parser.execute('entry')
    assert len(node.seq) == 1
    assert node.seq[0].type == 'lex_text'
    assert node.seq[0].text == 'abc'
    with parser.stream as context:
        assert context.read_char() == 'd'
    # (todo) : error

## tests - Positive

def test_pos_simple_success() -> None:
    """ simple valid case
    """
    parser = CrupyParserBase({
        'entry' : CrupyLexerOpSeq(
            CrupyLexerOpText('abc'),
            CrupyLexerAssertLookaheadPositive(
                CrupyLexerOpText('d'),
                CrupyLexerOpText('e'),
            ),
        ),
    })
    parser.register_stream('abcdezbcdz')
    node = parser.execute('entry')
    assert len(node.seq) == 1
    assert node.seq[0].type == 'lex_text'
    assert node.seq[0].text == 'abc'
    with parser.stream as context:
        assert context.read_char() == 'd'
    # (todo) : error
