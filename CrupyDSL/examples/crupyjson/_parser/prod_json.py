"""
crupyjson._parser.json   - handle json production
"""
__all__ = [
    'json_parser_prod_hook_json',
]
from typing import cast

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

def json_parser_prod_hook_json(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
    """ handle `json` node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 2
    assert node.seq[0].type == 'json_statement'
    assert node.seq[1].type == 'builtin_eof'
    return cast(CrupyDSLParserNodeBase, node.seq[0])
