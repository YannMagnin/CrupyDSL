"""
tests.lexer.assert_lookahead  - test for the CrupyLexerAssertLookahead*
"""
__all__ = (
    'CrupyUnittestLexerLookahead',
)

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core.parser import CrupyParserBase
from crupydslparser.core._lexer import (
    CrupyLexerOpSeq,
    CrupyLexerOpText,
    CrupyLexerAssertLookaheadNegative,
    CrupyLexerAssertLookaheadPositive,
)

#---
# Public
#---

class CrupyUnittestLexerLookahead(CrupyUnittestBase):
    """ unittest suite for the crupy lexer sequence operation
    """

    #---
    # Public tests
    #---

    ## Negative

    def test_neg_simple_success(self) -> None:
        """ simple valid case """
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
        self.assertEqual(len(node.seq), 1)
        self.assertEqual(node.seq[0].type, 'lex_text')
        self.assertEqual(node.seq[0].text, 'abc')
        with parser.stream as context:
            self.assertEqual(context.read_char(), 'd')
        # (todo) : error

    ## Positive

    def test_pos_simple_success(self) -> None:
        """ simple valid case """
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
        self.assertEqual(len(node.seq), 1)
        self.assertEqual(node.seq[0].type, 'lex_text')
        self.assertEqual(node.seq[0].text, 'abc')
        with parser.stream as context:
            self.assertEqual(context.read_char(), 'd')
        # (todo) : error
