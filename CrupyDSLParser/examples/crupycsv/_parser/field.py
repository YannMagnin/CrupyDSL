"""
crupydslparser.core._parser.field   - `field` production definition
"""
__all__ = [
    'csv_parser_prod_field_hook',
]

from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Public
#---

def csv_parser_prod_field_hook(
    parser: CrupyParserBase,
    node:   CrupyParserNode,
) -> CrupyParserNode:
    """ generate more appropriate node concerning `field` output

    @note
    - field        ::= <quoted_content> | <simple_content>
    - field_quoted ::= "\"" (<letter>|<digit>|<symbol>|<space>)+ "\""
    - field_simple ::= ((?!,)(<letter>|<digit>|<symbol>))*
    """
    print('!!! CSV field production hook invoked')
    print(f"> parser = {parser}")
    print(f"> node = {node}")
    return node
