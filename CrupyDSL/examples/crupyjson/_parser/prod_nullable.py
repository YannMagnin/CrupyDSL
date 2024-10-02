"""
crupyjson._parser.nullable  - handle nullable production
"""
__all__ = [
    'CrupyDSLParserNodeJsonNullable',
    'json_parser_prod_hook_nullable',
]

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeJsonNullable(CrupyDSLParserNodeBase):
    """ JSON "nullable" node

    @note
    we only need to have the node name to nullable, because we do not need
    to capture anything
    """

def json_parser_prod_hook_nullable(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
    """ handle `nullable` node
    """
    assert node.type == 'lex_text'
    assert node.text == 'null'
    return CrupyDSLParserNodeJsonNullable(
        parent_node = node,
    )
