"""
tests.lexer.assert_eof  - test the CrupyLexerAssertEOF
"""
__all__ = (
    'CrupyUnittestLexerAssertEof',
)

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpSeq,
    CrupyLexerOpText,
    CrupyLexerAssertEOF,
)

#---
# Public
#---

class CrupyUnittestLexerAssertEof(CrupyUnittestBase):
    """ unittest suite for cruper lexer end-of-file assertion
    """

    #---
    # Public test
    #---

    def test_eof_simple(self) -> None:#
        """ simple test case """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpSeq(
                CrupyLexerOpText('a'),
                CrupyLexerAssertEOF(),
            )
        })
        parser.register_stream('a')
        node = parser.execute('entry')
        self.assertEqual(node.type, 'lex_seq')
        self.assertEqual(len(node.seq), 1)
        self.assertEqual(node.seq[0].type, 'lex_text')
        self.assertEqual(node.seq[0].text, 'a')
        # (todo) : error
