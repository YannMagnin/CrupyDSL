"""
crupydslparser.core._dsl._parser.space  - DSL space hook
"""
__all__ = (
    'dsl_space_hook',
)

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeDslSpace(CrupyParserNode):
    """ space node

    @note
    we only need to have the node name to "dsl_space" since we do not need
    to capture anything
    """

def dsl_space_hook(node: CrupyParserNode) -> CrupyParserNode:
    """ handle "space" node
    """
    return CrupyParserNodeDslSpace(
        parent_node = node,
    )
