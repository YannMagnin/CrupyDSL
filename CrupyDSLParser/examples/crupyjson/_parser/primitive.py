"""
crupyjson._parser.primitive  - handle `primitive` production
"""
__all__ = [
    'CrupyParserNodeJsonPrimitive',
    'json_parser_prod_hook_primitive',
]

from crupydslparser.core.parser import (
    CrupyParserNode,
    CrupyParserException,
)

#---
# Public
#---

class CrupyParserNodeJsonPrimitive(CrupyParserNode):
    """ JSON "primitive" node
    """
    kind:   str
    data:   str|bool|None

def json_parser_prod_hook_primitive(node: CrupyParserNode) -> CrupyParserNode:
    """ handle `primitive` node
    """
    if node['name'] in ['lex_text', 'json_string']:
        return CrupyParserNodeJsonPrimitive(
            parent_node = node,
            kind        = node['name'].split('_')[1],
            data        = node['text'],
        )
    if node['name'] == 'json_nullable':
        return CrupyParserNodeJsonPrimitive(
            parent_node = node,
            kind        = 'nullable',
            data        = None,
        )
    if node['name'] == 'json_boolean':
        return CrupyParserNodeJsonPrimitive(
            parent_node = node,
            kind        = 'boolean',
            data        = node['state'],
        )
    raise CrupyParserException(
        f"Unable to handle JSON hook transformation, unknown node {node}"
    )
