"""
crupyjson._parser.array   - handle array production
"""
__all__ = [
    'json_parser_prod_hook_array',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeJsonArray(CrupyParserNode):
    """ `array` production node """
    node_list:  list[CrupyParserNode]

def json_parser_prod_hook_array(node: CrupyParserNode) -> CrupyParserNode:
    """ handle `array` node
    """
    assert node['name'] == 'lex_seq'
    assert len(node['seq']) == 4
    assert node['seq'][0]['name'] == 'lex_text'
    assert node['seq'][0]['text'] == '['
    assert node['seq'][1]['name'] == 'json_statement'
    assert node['seq'][2]['name'] == 'lex_rep'
    assert node['seq'][3]['name'] == 'lex_text'
    assert node['seq'][3]['text'] == ']'
    node_list = [node['seq'][1]]
    for stmt_info in node['seq'][1]['rep']:
        assert len(stmt_info) == 2
        assert stmt_info[0]['name'] == 'lex_text'
        assert stmt_info[0]['text'] == ','
        assert stmt_info[1]['name'] == 'json_statement'
        node_list.append(stmt_info[1])
    return CrupyParserNodeJsonArray(
        parent_node = node,
        node_list   = node_list,
    )
