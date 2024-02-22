"""
crupydslparser.core._parser.csv     - `csv` production definition
"""
__all__ = [
    'csv_parser_prod_csv_hook',
]
from typing import List

from crupycsv._parser.record import CrupyParserNodeCsvRecord
from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeCsv(CrupyParserNode):
    """ CSV general node """
    records:    List[CrupyParserNodeCsvRecord]

def csv_parser_prod_csv_hook(node: CrupyParserNode) -> CrupyParserNode:
    """ generate more appropriate node concerning `csv` output

    @note
    - production -> "cvs ::= (<record> "\n")+"
    """
    assert node['name'] == 'lex_rep'
    assert len(node['rep']) >= 1
    record_list: List[CrupyParserNodeCsvRecord] = []
    for record in node['rep']:
        assert len(record) == 1
        assert len(record[0]['seq']) == 2
        assert record[0]['seq'][0]['name'] == 'csv_record'
        assert record[0]['seq'][1]['name'] == 'lex_text'
        assert record[0]['seq'][1]['text'] == '\n'
        record_list.append(record[0]['seq'][0])
    return CrupyParserNodeCsv(
        stream_ctx  = node.stream_context,
        records     = record_list,
    )
