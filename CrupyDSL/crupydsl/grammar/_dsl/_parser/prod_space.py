"""
crupydsl.grammar._dsl._parser.space  - DSL space hook
"""
__all__ = [
    'CrupyDSLParserNodeDslSpace',
    'dsl_space_hook',
]

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeDslSpace(CrupyDSLParserNodeBase):
    """ space node

    @note
    we only need to have the node name to "dsl_space" since we do not need
    to capture anything
    """

def dsl_space_hook(node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
    """ handle "space" node
    """
    return CrupyDSLParserNodeDslSpace(
        parent_node = node,
    )
