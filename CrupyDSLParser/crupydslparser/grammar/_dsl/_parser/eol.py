"""
crupydslparser.grammar._dsl._parser.eol  - DSL eol hook
"""
__all__ = [
    'dsl_eol_hook',
]

from crupydslparser.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeDslEol(CrupyParserNode):
    """ eol node

    @note
    we only need to have the node name to "dsl_eol" since we do not need
    to capture anything
    """

def dsl_eol_hook(node: CrupyParserNode) -> CrupyParserNode:
    """ handle "eol" node
    """
    return CrupyParserNodeDslEol(
        parent_node = node,
    )
