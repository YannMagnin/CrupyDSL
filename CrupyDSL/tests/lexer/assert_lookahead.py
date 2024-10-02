"""
tests.lexer.assert_lookahead  - test for the CrupyDSLLexerAssertLookahead*
"""
from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpSeq,
    CrupyDSLLexerOpText,
    CrupyDSLLexerAssertLookaheadNegative,
    CrupyDSLLexerAssertLookaheadPositive,
)

#---
# Public
#---

## tests - Negative

def test_neg_simple_success() -> None:
    """ simple valid case
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpText('abc'),
            CrupyDSLLexerAssertLookaheadNegative(
                CrupyDSLLexerOpText('d'),
                CrupyDSLLexerOpText('r'),
                CrupyDSLLexerOpText('x'),
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
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpText('abc'),
            CrupyDSLLexerAssertLookaheadPositive(
                CrupyDSLLexerOpText('d'),
                CrupyDSLLexerOpText('e'),
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
