"""
crupydslparser._dsl._parser.string  - handle string production
"""
__all__ = [
    'dsl_string_hook',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeDslString(CrupyParserNode):
    """ DSL "string" node """
    text:   str

def dsl_string_hook(node: CrupyParserNode) -> CrupyParserNode:
    """ handle `string` node
    """
    assert node['name'] == 'lex_seq'
    assert len(node['seq']) == 3
    assert node['seq'][0]['name'] == 'lex_text'
    assert node['seq'][1]['name'] == 'lex_rep'
    assert node['seq'][2]['name'] == 'lex_text'
    assert node['seq'][0]['text'] == '"'
    assert node['seq'][2]['text'] == '"'
    text = ''
    for seq in node['seq'][1]['rep']:
        assert len(seq) == 1
        assert seq[0]['name'] == 'lex_text'
        text += seq[0]['text']
    return CrupyParserNodeDslString(
        parent_node = node,
        text        = text,
    )
