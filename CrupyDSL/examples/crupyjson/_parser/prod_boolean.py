"""
crupyjson._parser.boolean   - handle boolean production
"""
__all__ = [
    'CrupyDSLParserNodeJsonBoolean',
    'json_parser_prod_hook_boolean',
]

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeJsonBoolean(CrupyDSLParserNodeBase):
    """ JSON "boolean" node """
    state:  bool

def json_parser_prod_hook_boolean(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
    """ handle `boolean` node
    """
    assert node.type == 'lex_text'
    assert node.text in ['true', 'false']
    return CrupyDSLParserNodeJsonBoolean(
        parent_node = node,
        state       = node.text == 'true',
    )
