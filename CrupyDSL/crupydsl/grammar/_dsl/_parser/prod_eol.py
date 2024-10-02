"""
crupydsl.grammar._dsl._parser.eol  - DSL eol hook
"""
__all__ = [
    'CrupyDSLParserNodeDslEol',
    'dsl_eol_hook',
]

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeDslEol(CrupyDSLParserNodeBase):
    """ eol node

    @note
    we only need to have the node name to "dsl_eol" since we do not need
    to capture anything
    """

def dsl_eol_hook(node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
    """ handle "eol" node
    """
    return CrupyDSLParserNodeDslEol(
        parent_node = node,
    )
