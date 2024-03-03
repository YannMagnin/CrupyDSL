"""
crupyjson._parser.string    - handle string production
"""
__all__ = [
    'CrupyParserNodeJsonString',
    'json_parser_prod_hook_string',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeJsonString(CrupyParserNode):
    """ JSON "string" node """
    text:   str

def json_parser_prod_hook_string(node: CrupyParserNode) -> CrupyParserNode:
    """ handle `string` node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'lex_text'
    assert node.seq[1].type == 'lex_rep'
    assert node.seq[2].type == 'lex_text'
    assert node.seq[0].text == node.seq[2].text
    assert node.seq[0].text in ['"', '\'']
    text = ''
    for seq in node.seq[1].rep:
        assert len(seq) == 1
        assert seq[0].type == 'lex_text'
        text += seq[0].text
    return CrupyParserNodeJsonString(
        parent_node = node,
        text        = text,
    )
