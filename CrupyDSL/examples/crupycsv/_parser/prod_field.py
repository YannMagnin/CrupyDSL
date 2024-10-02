"""
crupydsl.core._parser.field   - `field` production definition
"""
__all__ = [
    'csv_parser_prod_field_hook',
    'CrupyDSLParserNodeCsvField',
]

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Internals
#---

def __check_node_simple(node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
    """ field simple node check
    """
    assert node.type == 'lex_rep'
    capture = ''
    for rep in node.rep:
        assert len(rep) == 1
        op = rep[0]
        assert op.type == 'lex_seq'
        assert len(op.seq) == 1
        assert op.seq[0].type == 'lex_text'
        capture += op.seq[0].text
    return CrupyDSLParserNodeCsvField(
        parent_node = node,
        kind        = 'simple',
        text        = capture,
    )

def __check_node_quoted(node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
    """ generic node check """
    assert node.type == 'lex_between'
    assert node.captured_start.type == 'lex_text'
    assert node.captured_end.type == 'lex_text'
    return CrupyDSLParserNodeCsvField(
        parent_node = node,
        kind        = 'quoted',
        text        = node.captured_middle,
    )

#---
# Public
#---

class CrupyDSLParserNodeCsvField(CrupyDSLParserNodeBase):
    """ CSV field information """
    kind:   str
    text:   str

def csv_parser_prod_field_hook(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
    """ generate more appropriate node concerning `field` output

    @note
    - field        ::= <quoted_content> | <simple_content>
    - field_quoted ::= "\"" (<letter>|<digit>|<symbol>|<space>)+ "\""
    - field_simple ::= ((?!,)(<letter>|<digit>|<symbol>))*
    """
    try:
        return __check_node_simple(node)
    except AssertionError:
        return __check_node_quoted(node)
