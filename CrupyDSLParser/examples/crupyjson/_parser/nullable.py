"""
crupyjson._parser.nullable  - handle nullable production
"""
__all__ = [
    'CrupyParserNodeJsonNullable',
    'json_parser_prod_hook_nullable',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeJsonNullable(CrupyParserNode):
    """ JSON "nullable" node

    @note
    we only need to have the node name to nullable, because we do not need
    to capture anything
    """

def json_parser_prod_hook_nullable(node: CrupyParserNode) -> CrupyParserNode:
    """ handle `nullable` node
    """
    assert node.type == 'lex_text'
    assert node.text == 'null'
    return CrupyParserNodeJsonNullable(
        parent_node = node,
    )
