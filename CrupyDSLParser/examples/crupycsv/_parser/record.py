"""
crupydslparser.core._parser.record  - `record` production definition
"""
__all__ = [
    'csv_parser_prod_record_hook',
    'CrupyParserNodeCsvRecord',
]
from typing import List

from crupydslparser.parser import CrupyParserNodeBase
from crupycsv._parser.field import CrupyParserNodeCsvField

#---
# Public
#---

class CrupyParserNodeCsvRecord(CrupyParserNodeBase):
    """ record information """
    fields: List[CrupyParserNodeCsvField]

def csv_parser_prod_record_hook(
    node: CrupyParserNodeBase,
) -> CrupyParserNodeBase:
    """ generate more appropriate node concerning `record` output

    @note
    - record ::= <field> ("," <field>)*
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 2
    assert node.seq[0].type == 'csv_field'
    assert node.seq[1].type == 'lex_rep'
    field_list = [node.seq[0]]
    for field in node.seq[1].rep:
        assert len(field) == 2
        assert field[0].type == 'lex_text'
        assert field[0].text == ','
        assert field[1].type == 'csv_field'
        field_list.append(field[1])
    return CrupyParserNodeCsvRecord(
        parent_node = node,
        fields      = field_list,
    )
