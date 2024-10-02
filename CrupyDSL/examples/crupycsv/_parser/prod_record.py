"""
crupydsl.core._parser.record  - `record` production definition
"""
__all__ = [
    'csv_parser_prod_record_hook',
    'CrupyDSLParserNodeCsvRecord',
]
from typing import List

from crupydsl.parser import CrupyDSLParserNodeBase
from crupycsv._parser.prod_field import CrupyDSLParserNodeCsvField

#---
# Public
#---

class CrupyDSLParserNodeCsvRecord(CrupyDSLParserNodeBase):
    """ record information """
    fields: List[CrupyDSLParserNodeCsvField]

def csv_parser_prod_record_hook(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
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
    return CrupyDSLParserNodeCsvRecord(
        parent_node = node,
        fields      = field_list,
    )
