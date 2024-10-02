"""
crupyjson._parser.container   - handle container production
"""
__all__ = [
    'json_parser_prod_hook_container',
    'CrupyDSLParserNodeJsonContainer',
]

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeJsonContainer(CrupyDSLParserNodeBase):
    """ JSON "container" node
    """
    kind: str
    node: CrupyDSLParserNodeBase

def json_parser_prod_hook_container(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
    """ handle `container` node
    """
    assert node.type in ['json_array', 'json_object']
    return CrupyDSLParserNodeJsonContainer(
        parent_node = node,
        kind        = node.type,
        node        = node,
    )
