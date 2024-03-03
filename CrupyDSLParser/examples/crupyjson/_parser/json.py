"""
crupyjson._parser.json   - handle json production
"""
__all__ = [
    'json_parser_prod_hook_json',
]
from typing import cast

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

def json_parser_prod_hook_json(node: CrupyParserNode) -> CrupyParserNode:
    """ handle `json` node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 1
    assert node.seq[0].type == 'json_statement'
    return cast(CrupyParserNode, node.seq[0])
