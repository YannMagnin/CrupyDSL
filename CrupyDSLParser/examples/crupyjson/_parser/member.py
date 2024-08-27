"""
crupyjson._parser.member   - handle object production
"""
__all__ = [
    'json_parser_prod_hook_member',
]

from crupydslparser.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeJsonMember(CrupyParserNodeBase):
    """ `array` production node """
    key:    str
    value:  CrupyParserNodeBase

def json_parser_prod_hook_member(
    node: CrupyParserNodeBase,
) -> CrupyParserNodeBase:
    """ handle `array` node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 5
    assert node.seq[0].type == 'json_string'
    assert node.seq[2].type == 'lex_text'
    assert node.seq[2].text == ':'
    assert node.seq[4].type == 'json_statement'
    value = node.seq[4].node
    if value.type == 'json_container':
        value = value.node
    return CrupyParserNodeJsonMember(
        parent_node = node,
        key         = node.seq[0].text,
        value       = value,
    )
