"""
crupyjson._parser.member   - handle object production
"""
__all__ = [
    'json_parser_prod_hook_member',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeJsonMember(CrupyParserNode):
    """ `array` production node """
    key:    str
    value:  CrupyParserNode

def json_parser_prod_hook_member(node: CrupyParserNode) -> CrupyParserNode:
    """ handle `array` node
    """
    assert node['name'] == 'lex_seq'
    assert len(node['seq']) == 3
    assert node['seq'][0]['name'] == 'json_string'
    assert node['seq'][1]['name'] == 'lex_text'
    assert node['seq'][1]['text'] == ':'
    assert node['seq'][2]['name'] == 'json_statement'
    value = node['seq'][2]['node']
    if value['name'] == 'json_container':
        value = value['node']
    return CrupyParserNodeJsonMember(
        parent_node = node,
        key         = node['seq'][0]['text'],
        value       = value,
    )
