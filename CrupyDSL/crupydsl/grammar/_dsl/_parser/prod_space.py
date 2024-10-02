"""
crupydsl.grammar._dsl._parser.space  - DSL space hook
"""
__all__ = [
    'CrupyParserNodeDslSpace',
    'dsl_space_hook',
]

from crupydsl.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeDslSpace(CrupyParserNodeBase):
    """ space node

    @note
    we only need to have the node name to "dsl_space" since we do not need
    to capture anything
    """

def dsl_space_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle "space" node
    """
    return CrupyParserNodeDslSpace(
        parent_node = node,
    )
