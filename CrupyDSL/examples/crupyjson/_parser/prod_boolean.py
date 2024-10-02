"""
crupyjson._parser.boolean   - handle boolean production
"""
__all__ = [
    'CrupyParserNodeJsonBoolean',
    'json_parser_prod_hook_boolean',
]

from crupydsl.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeJsonBoolean(CrupyParserNodeBase):
    """ JSON "boolean" node """
    state:  bool

def json_parser_prod_hook_boolean(
    node: CrupyParserNodeBase,
) -> CrupyParserNodeBase:
    """ handle `boolean` node
    """
    assert node.type == 'lex_text'
    assert node.text in ['true', 'false']
    return CrupyParserNodeJsonBoolean(
        parent_node = node,
        state       = node.text == 'true',
    )
