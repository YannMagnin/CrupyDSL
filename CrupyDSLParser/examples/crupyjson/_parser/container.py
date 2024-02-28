"""
crupyjson._parser.container   - handle container production
"""
__all__ = [
    'json_parser_prod_hook_container',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

def json_parser_prod_hook_container(node: CrupyParserNode) -> CrupyParserNode:
    """ handle `container` node
    """
    assert node['name'] in ['json_array', 'json_object']
    return node
