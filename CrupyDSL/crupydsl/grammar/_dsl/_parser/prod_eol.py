"""
crupydsl.grammar._dsl._parser.eol  - DSL eol hook
"""
__all__ = [
    'CrupyParserNodeDslEol',
    'dsl_eol_hook',
]

from crupydsl.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeDslEol(CrupyParserNodeBase):
    """ eol node

    @note
    we only need to have the node name to "dsl_eol" since we do not need
    to capture anything
    """

def dsl_eol_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle "eol" node
    """
    return CrupyParserNodeDslEol(
        parent_node = node,
    )
