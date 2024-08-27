"""
crupyjson._parser.json   - handle json production
"""
__all__ = [
    'json_parser_prod_hook_json',
]
from typing import cast

from crupydslparser.parser import CrupyParserNodeBase

#---
# Public
#---

def json_parser_prod_hook_json(
    node: CrupyParserNodeBase,
) -> CrupyParserNodeBase:
    """ handle `json` node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'json_statement'
    assert node.seq[2].type == 'builtin_eof'
    return cast(CrupyParserNodeBase, node.seq[0])
