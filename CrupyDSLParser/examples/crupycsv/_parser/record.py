"""
crupydslparser.core._parser.record  - `record` production definition
"""
__all__ = [
    'csv_parser_prod_record_hook',
]

from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Public
#---

def csv_parser_prod_record_hook(
    parser: CrupyParserBase,
    node:   CrupyParserNode,
) -> CrupyParserNode:
    """ generate more appropriate node concerning `record` output

    @note
    - record ::= <field> ("," <field>)*
    """
    print('!!! CSV record production hook invoked')
    print(f"> parser = {parser}")
    print(f"> node = {node}")
    return node
