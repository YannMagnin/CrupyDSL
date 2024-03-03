"""
crupyjson._parser.statement  - handle statement production
"""
__all__ = [
    'json_parser_prod_hook_statement',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeJsonStatement(CrupyParserNode):
    """ JSON "statement" node

    @note
    we only need to have the node name to statement, because we do not need
    to capture anything
    """
    node: CrupyParserNode

def json_parser_prod_hook_statement(
    node: CrupyParserNode,
) -> CrupyParserNode:
    """ handle `statement` node
    """
    assert node.type in ['json_primitive', 'json_container']
    return CrupyParserNodeJsonStatement(
        parent_node = node,
        node        = node,
    )
