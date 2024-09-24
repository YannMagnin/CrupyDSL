"""
tests.lexer.op_optional     - test the CrupyLexerOpOptional
"""
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpText,
    CrupyLexerOpOptional,
    CrupyLexerOpSeq,
)

#---
# Internals
#---

def __check_node(node: CrupyParserNodeBase, text: str) -> None:
    """ check and return captured information
    """
    content = ''
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'lex_text'
    content += node.seq[0].text
    assert node.seq[1].type == 'lex_optional'
    if node.seq[1].seq:
        assert len(node.seq[1].seq) == 1
        assert node.seq[1].seq[0].type == 'lex_text'
        content += node.seq[1].seq[0].text
    assert node.seq[2].type == 'lex_text'
    content += node.seq[2].text
    assert content == text

#---
# Public
#---

def test_simple_success() -> None:
    """ simple valid cases
    """
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
    __check_node(parser.execute('entry'), 'http://')
    parser.register_stream('https://')
    __check_node(parser.execute('entry'), 'https://')
