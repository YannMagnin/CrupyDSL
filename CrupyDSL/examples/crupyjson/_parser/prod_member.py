"""
crupyjson._parser.member   - handle object production
"""
__all__ = [
    'json_parser_prod_hook_member',
    'CrupyDSLParserNodeJsonMember',
]

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeJsonMember(CrupyDSLParserNodeBase):
    """ `array` production node """
    key:    str
    value:  CrupyDSLParserNodeBase

def json_parser_prod_hook_member(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
    """ handle `array` node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'json_string'
    assert node.seq[1].type == 'lex_text'
    assert node.seq[1].text == ':'
    assert node.seq[2].type == 'json_statement'
    value = node.seq[2].node
    if value.type == 'json_container':
        value = value.node
    return CrupyDSLParserNodeJsonMember(
        parent_node = node,
        key         = node.seq[0].text,
        value       = value,
    )
