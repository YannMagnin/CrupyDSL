"""
crupyjson._parser.object   - handle object production
"""
__all__ = [
    'json_parser_prod_hook_object',
]

from crupydslparser.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeJsonObject(CrupyParserNodeBase):
    """ `array` production node """
    members:  list[CrupyParserNodeBase]

def json_parser_prod_hook_object(
    node: CrupyParserNodeBase,
) -> CrupyParserNodeBase:
    """ handle `array` node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 8
    assert node.seq[1].type == 'lex_text'
    assert node.seq[1].text == '{'
    assert node.seq[3].type == 'json_member'
    assert node.seq[4].type == 'lex_rep'
    assert node.seq[6].type == 'lex_text'
    assert node.seq[6].text == '}'
    node_list = [node.seq[3]]
    for stmt_info in node.seq[4].rep:
        assert len(stmt_info) == 4
        assert stmt_info[1].type == 'lex_text'
        assert stmt_info[1].text == ','
        assert stmt_info[3].type == 'json_member'
        node_list.append(stmt_info[3])
    return CrupyParserNodeJsonObject(
        parent_node = node,
        members     = node_list,
    )
