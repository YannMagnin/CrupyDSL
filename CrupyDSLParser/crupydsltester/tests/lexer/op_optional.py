"""
tests.lexer.op_optional     - test the CrupyLexerOpOptional
"""
__all__ = (
    'CrupyUnittestLexerOptional',
)

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpText,
    CrupyLexerOpOptional,
    CrupyLexerOpSeq,
)

#---
# Public
#---

class CrupyUnittestLexerOptional(CrupyUnittestBase):
    """ unittest suite for the crupy lexer text operation
    """

    #---
    # Internals
    #---

    def __check_node(self, node: CrupyParserNodeBase, text: str) -> None:
        """ check and return captured information
        """
        content = ''
        self.assertEqual(node.type, 'lex_seq')
        self.assertEqual(len(node.seq), 3)
        self.assertEqual(node.seq[0].type, 'lex_text')
        content += node.seq[0].text
        self.assertEqual(node.seq[1].type, 'lex_optional')
        if node.seq[1].seq:
            self.assertEqual(len(node.seq[1].seq), 1)
            self.assertEqual(node.seq[1].seq[0].type, 'lex_text')
            content += node.seq[1].seq[0].text
        self.assertEqual(node.seq[2].type, 'lex_text')
        content += node.seq[2].text
        self.assertEqual(content, text)

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry' : \
                CrupyLexerOpSeq(
                    CrupyLexerOpText('http'),
                    CrupyLexerOpOptional(
                        CrupyLexerOpText('s'),
                    ),
                    CrupyLexerOpText('://'),
                ),
        })
        parser.register_stream('http://')
        self.__check_node(parser.execute('entry'), 'http://')
        parser.register_stream('https://')
        self.__check_node(parser.execute('entry'), 'https://')
