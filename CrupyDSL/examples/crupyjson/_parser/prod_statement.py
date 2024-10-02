"""
crupyjson._parser.statement  - handle statement production
"""
__all__ = [
    'json_parser_prod_hook_statement',
    'CrupyDSLParserNodeJsonStatement',
]

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeJsonStatement(CrupyDSLParserNodeBase):
    """ JSON "statement" node

    @note
    we only need to have the node name to statement, because we do not need
    to capture anything
    """
    node: CrupyDSLParserNodeBase

def json_parser_prod_hook_statement(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
    """ handle `statement` node
    """
    assert node.type in ['json_primitive', 'json_container']
    return CrupyDSLParserNodeJsonStatement(
        parent_node = node,
        node        = node,
    )
