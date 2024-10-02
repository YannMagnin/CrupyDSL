"""
crupyjson._parser.primitive  - handle `primitive` production
"""
__all__ = [
    'CrupyDSLParserNodeJsonPrimitive',
    'json_parser_prod_hook_primitive',
]
from typing import Union

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeJsonPrimitive(CrupyDSLParserNodeBase):
    """ JSON "primitive" node
    """
    kind:   str
    data:   Union[str, bool, None]

def json_parser_prod_hook_primitive(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
    """ handle `primitive` node
    """
    if node.type == 'lex_text':
        return CrupyDSLParserNodeJsonPrimitive(
            parent_node = node,
            kind        = 'digit',
            data        = node.text,
        )
    if node.type == 'json_string':
        return CrupyDSLParserNodeJsonPrimitive(
            parent_node = node,
            kind        = 'string',
            data        = node.text,
        )
    if node.type == 'json_nullable':
        return CrupyDSLParserNodeJsonPrimitive(
            parent_node = node,
            kind        = 'nullable',
            data        = None,
        )
    assert node.type == 'json_boolean'
    return CrupyDSLParserNodeJsonPrimitive(
        parent_node = node,
        kind        = 'boolean',
        data        = node.state,
    )
