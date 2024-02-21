"""
crupydslparser.core._parser.csv     - `csv` production definition
"""
__all__ = [
    'csv_parser_prod_csv_hook',
]

from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Public
#---

def csv_parser_prod_csv_hook(
    parser: CrupyParserBase,
    node:   CrupyParserNode,
) -> CrupyParserNode:
    """ generate more appropriate node concerning `csv` output

    @note
    - production -> "cvs ::= (<record> "\n")+"
    """
    print('!!! CSV final production hook invoked')
    print(f"> parser = {parser}")
    print(f"> node = {node}")
    return node
