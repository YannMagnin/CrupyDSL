"""
crupyjson._parser.boolean   - handle boolean production
"""
__all__ = [
    'CrupyParserNodeJsonBoolean',
    'json_parser_prod_hook_boolean',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeJsonBoolean(CrupyParserNode):
    """ JSON "boolean" node """
    state:  bool

def json_parser_prod_hook_boolean(node: CrupyParserNode) -> CrupyParserNode:
    """ handle `boolean` node
    """
    assert node['name'] == 'lex_text'
    assert node['text'] in ['true', 'false']
    return CrupyParserNodeJsonBoolean(
        parent_node = node,
        state       = node['text'] == 'true',
    )
