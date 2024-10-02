"""
crupyjson._parser.array   - handle array production
"""
__all__ = [
    'json_parser_prod_hook_array',
    'CrupyParserNodeJsonArray',
]
from typing import cast

from crupydsl.parser import CrupyParserNodeBase

#---
# Internals
#---

def _resolve_node(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ resolve node to a more appropriate node
    """
    assert node.type == 'json_statement'
    if node.node.type == 'json_primitive':
        return cast(CrupyParserNodeBase, node.node)
    if node.node.node.type == 'json_container':
        return cast(CrupyParserNodeBase, node.node.node)
    return node

#---
# Public
#---

class CrupyParserNodeJsonArray(CrupyParserNodeBase):
    """ `array` production node """
    node_list:  list[CrupyParserNodeBase]

def json_parser_prod_hook_array(
    node: CrupyParserNodeBase,
) -> CrupyParserNodeBase:
    """ handle `array` node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 4
    assert node.seq[0].type == 'lex_text'
    assert node.seq[0].text == '['
    assert node.seq[1].type == 'json_statement'
    assert node.seq[2].type == 'lex_rep'
    assert node.seq[3].type == 'lex_text'
    assert node.seq[3].text == ']'
    node_list = [_resolve_node(node.seq[1])]
    for stmt_info in node.seq[2].rep:
        assert len(stmt_info) == 2
        assert stmt_info[0].type == 'lex_text'
        assert stmt_info[0].text == ','
        assert stmt_info[1].type == 'json_statement'
        node_list.append(_resolve_node(stmt_info[1]))
    return CrupyParserNodeJsonArray(
        parent_node = node,
        node_list   = node_list,
    )
