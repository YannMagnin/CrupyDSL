"""
crupyjson._parser.container   - handle container production
"""
__all__ = [
    'json_parser_prod_hook_container',
    'CrupyParserNodeJsonContainer',
]

from crupydsl.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeJsonContainer(CrupyParserNodeBase):
    """ JSON "container" node
    """
    kind: str
    node: CrupyParserNodeBase

def json_parser_prod_hook_container(
    node: CrupyParserNodeBase,
) -> CrupyParserNodeBase:
    """ handle `container` node
    """
    assert node.type in ['json_array', 'json_object']
    return CrupyParserNodeJsonContainer(
        parent_node = node,
        kind        = node.type,
        node        = node,
    )
