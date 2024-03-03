"""
crupyjson._parser.object   - handle object production
"""
__all__ = [
    'json_parser_prod_hook_object',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeJsonObject(CrupyParserNode):
    """ `array` production node """
    members:  list[CrupyParserNode]

def json_parser_prod_hook_object(node: CrupyParserNode) -> CrupyParserNode:
    """ handle `array` node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 4
    assert node.seq[0].type == 'lex_text'
    assert node.seq[0].text == '{'
    assert node.seq[1].type == 'json_member'
    assert node.seq[2].type == 'lex_rep'
    assert node.seq[3].type == 'lex_text'
    assert node.seq[3].text == '}'
    node_list = [node.seq[1]]
    for stmt_info in node.seq[2].rep:
        assert len(stmt_info) == 2
        assert stmt_info[0].type == 'lex_text'
        assert stmt_info[0].text == ','
        assert stmt_info[1].type == 'json_member'
        node_list.append(stmt_info[1])
    return CrupyParserNodeJsonObject(
        parent_node = node,
        members     = node_list,
    )
