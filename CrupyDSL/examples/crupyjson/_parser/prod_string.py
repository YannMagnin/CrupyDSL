"""
crupyjson._parser.string    - handle string production
"""
__all__ = [
    'CrupyParserNodeJsonString',
    'json_parser_prod_hook_string',
]

from crupydsl.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeJsonString(CrupyParserNodeBase):
    """ JSON "string" node """
    text:   str

def json_parser_prod_hook_string(
    node: CrupyParserNodeBase,
) -> CrupyParserNodeBase:
    """ handle `string` node
    """
    assert node.type == 'lex_between'
    assert node.captured_start.type == 'lex_text'
    assert node.captured_start.text in ('"', "'")
    assert node.captured_end.type == 'lex_text'
    assert node.captured_end.text in ('"', "'")
    return CrupyParserNodeJsonString(
        parent_node = node,
        text        = node.captured_middle,
    )
