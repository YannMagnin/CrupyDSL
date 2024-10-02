"""
tests.lexer.op_optional     - test the CrupyDSLLexerOpOptional
"""
from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser.node import CrupyDSLParserNodeBase
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpOptional,
    CrupyDSLLexerOpSeq,
)

#---
# Internals
#---

def __check_node(node: CrupyDSLParserNodeBase, text: str) -> None:
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
    parser = CrupyDSLParserBase({
        'entry' : \
            CrupyDSLLexerOpSeq(
                CrupyDSLLexerOpText('http'),
                CrupyDSLLexerOpOptional(
                    CrupyDSLLexerOpText('s'),
                ),
                CrupyDSLLexerOpText('://'),
            ),
    })
    parser.register_stream('http://')
    __check_node(parser.execute('entry'), 'http://')
    parser.register_stream('https://')
    __check_node(parser.execute('entry'), 'https://')
