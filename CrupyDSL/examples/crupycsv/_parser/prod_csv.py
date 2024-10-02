"""
crupydsl.core._parser.csv     - `csv` production definition
"""
__all__ = [
    'csv_parser_prod_csv_hook',
    'CrupyDSLParserNodeCsv',
]
from typing import List

from crupycsv._parser.prod_record import CrupyDSLParserNodeCsvRecord
from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeCsv(CrupyDSLParserNodeBase):
    """ CSV general node """
    records:    List[CrupyDSLParserNodeCsvRecord]

def csv_parser_prod_csv_hook(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
    """ generate more appropriate node concerning `csv` output

    @note
    - production -> "cvs ::= (<record> "\n")+ :eof:"
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 2
    assert node.seq[1].type == 'builtin_eof'
    node = node.seq[0]
    assert node.type == 'lex_rep'
    assert len(node.rep) >= 1
    record_list: List[CrupyDSLParserNodeCsvRecord] = []
    for record in node.rep:
        assert len(record) == 1
        assert len(record[0].seq) == 2
        assert record[0].seq[0].type == 'csv_record'
        assert record[0].seq[1].type == 'lex_text'
        assert record[0].seq[1].text == '\n'
        record_list.append(record[0].seq[0])
    return CrupyDSLParserNodeCsv(
        parent_node = node,
        records     = record_list,
    )
