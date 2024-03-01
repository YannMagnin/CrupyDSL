"""
crupydslparser.core._dsl._parser.builtin  - DSL builtin hook
"""
__all__ = [
    'dsl_builtin_hook',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeDslBuiltin(CrupyParserNode):
    """ builtin node
    """
    kind:   str

def dsl_builtin_hook(node: CrupyParserNode) -> CrupyParserNode:
    """ handle "builtin" node
    """
    assert node['name'] == 'lex_seq'
    assert len(node['seq']) == 3
    assert node['seq'][0]['name'] == 'lex_text'
    assert node['seq'][0]['text'] == ':'
    assert node['seq'][2]['name'] == 'lex_text'
    assert node['seq'][2]['text'] == ':'
    assert node['seq'][1]['name'] == 'lex_rep'
    kind = ''
    for text in node['seq'][1]['rep']:
        assert len(text) == 1
        assert text[0]['name'] == 'lex_text'
        kind += text[0]['text']
    return CrupyParserNodeDslBuiltin(
        parent_node = node,
        kind        = kind,
    )