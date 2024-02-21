"""
tests.lexer.assert_lookahead  - tesy for the CrupyLexerAssertLookahead*
"""
__all__ = [
    'CrupyUnittestLexerLookahead',
]

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
                    CrupyLexerOpText('e'),
                ),
            ),
        })
        parser.register_stream('\tabcdr  abcde')
        node = parser.execute('entry')
        self.assertIsNotNone(node)
        if node is None:
            return
        self.assertEqual(len(node['seq']), 1)
        self.assertEqual(node['seq'][0]['name'], 'lex_text')
        self.assertEqual(node['seq'][0]['text'], 'abc')
        self.assertIsNone(parser.execute('entry'))

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
        parser.register_stream('\tabcde  abcdz')
        node = parser.execute('entry')
        self.assertIsNotNone(node)
        if node is None:
            return
        self.assertEqual(len(node['seq']), 1)
        self.assertEqual(node['seq'][0]['name'], 'lex_text')
        self.assertEqual(node['seq'][0]['text'], 'abc')
        self.assertIsNone(parser.execute('entry'))
