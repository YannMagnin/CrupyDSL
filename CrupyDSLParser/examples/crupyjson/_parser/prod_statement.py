"""
crupyjson._parser.statement  - handle statement production
"""
__all__ = [
    'json_parser_prod_hook_statement',
    'CrupyParserNodeJsonStatement',
]

from crupydslparser.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeJsonStatement(CrupyParserNodeBase):
    """ JSON "statement" node

    @note
    we only need to have the node name to statement, because we do not need
    to capture anything
    """
    node: CrupyParserNodeBase

def json_parser_prod_hook_statement(
    node: CrupyParserNodeBase,
) -> CrupyParserNodeBase:
    """ handle `statement` node
    """
    assert node.type in ['json_primitive', 'json_container']
    return CrupyParserNodeJsonStatement(
        parent_node = node,
        node        = node,
    )
