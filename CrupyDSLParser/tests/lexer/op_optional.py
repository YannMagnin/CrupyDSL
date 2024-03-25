"""
tests.lexer.op_optional     - test the CrupyLexerOpOptional
"""
__all__ = [
    'CrupyUnittestLexerOptional',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)
from crupydslparser.core._lexer import (
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

    def __check_node(self, node: CrupyParserNode|None, text: str) -> None:
        """ check and return captured information
        """
        content = ''
        self.assertIsNotNone(node)
        if node is None:
            return
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
        self.__check_node(parser.execute('entry', False), 'http://')
        parser.register_stream('https://')
        self.__check_node(parser.execute('entry', False), 'https://')
