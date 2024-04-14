"""
crupydslparser.grammar._dsl._parser.space  - DSL space hook
"""
__all__ = [
    'dsl_space_hook',
]

from crupydslparser.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeBaseDslSpace(CrupyParserNodeBase):
    """ space node

    @note
    we only need to have the node name to "dsl_space" since we do not need
    to capture anything
    """

def dsl_space_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle "space" node
    """
    return CrupyParserNodeBaseDslSpace(
        parent_node = node,
    )
