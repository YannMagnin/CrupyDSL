"""
crupyjson._parser.string    - handle string production
"""
__all__ = [
    'CrupyDSLParserNodeJsonString',
    'json_parser_prod_hook_string',
]

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeJsonString(CrupyDSLParserNodeBase):
    """ JSON "string" node """
    text:   str

def json_parser_prod_hook_string(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
    """ handle `string` node
    """
    assert node.type == 'lex_between'
    assert node.captured_start.type == 'lex_text'
    assert node.captured_start.text in ('"', "'")
    assert node.captured_end.type == 'lex_text'
    assert node.captured_end.text in ('"', "'")
    return CrupyDSLParserNodeJsonString(
        parent_node = node,
        text        = node.captured_middle,
    )
