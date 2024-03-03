"""
tests.lexer.assert_eof  - test the CrupyLexerAssertEOF
"""
__all__ = [
    'CrupyUnittestLexerAssertEOF',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core.parser import CrupyParserBase
from crupydslparser.core._lexer import (
    CrupyLexerOpSeq,
    CrupyLexerOpText,
    CrupyLexerAssertEOF,
)

#---
# Public
#---

class CrupyUnittestLexerAssertEOF(CrupyUnittestBase):
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
        self.assertIsNotNone(node)
        if node is None:
            return
        self.assertEqual(node.type, 'lex_seq')
        self.assertEqual(len(node.seq), 1)
        self.assertEqual(node.seq[0].type, 'lex_text')
        self.assertEqual(node.seq[0].text, 'a')
