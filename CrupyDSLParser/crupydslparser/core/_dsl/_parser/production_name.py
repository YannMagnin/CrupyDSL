"""
crupydslparser.core._dsl._parser.production_name  - DSL parser hook
"""
__all__ = [
    'dsl_production_name_hook',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Internals
#---

def __ensure_node_valid(node: CrupyParserNode) -> None:
    """ ensure that the given node is valid

    We should have the following tree:
    - node[]
    """
    assert node['name'] == 'lex_seq'
    assert len(node['seq']) == 3
    assert node['seq'][0]['name'] == 'lex_text'
    assert node['seq'][1]['name'] == 'lex_rep'
    assert node['seq'][2]['name'] == 'lex_text'
    assert len(node['seq'][1]['rep']) >= 1
    for text in node['seq'][1]['rep']:
        assert len(text) == 1
        assert text[0]['name'] == 'lex_text'

#---
# Public
#---

## special production name node

class CrupyParserNodeDslProdName(CrupyParserNode):
    """ production name node """
    production_name: str

## hook

def dsl_production_name_hook(node: CrupyParserNode) -> CrupyParserNode:
    """ hook the `crupy_dsl_production_name` production

    @note
    > production -> crupy_dsl_production_name ::= "<[a-z_]+>"
    > only keep the production name and ignore all other information
    """
    __ensure_node_valid(node)
    rule_name = ''
    for text in node['seq'][1]['rep']:
        rule_name += text[0]['text']
    return CrupyParserNodeDslProdName(
        stream_ctx      = node.stream_context,
        production_name = rule_name,
    )
