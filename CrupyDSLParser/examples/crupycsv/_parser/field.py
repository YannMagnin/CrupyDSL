"""
crupydslparser.core._parser.field   - `field` production definition
"""
__all__ = [
    'csv_parser_prod_field_hook',
    'CrupyParserNodeCsvField',
]

from crupydslparser.parser import CrupyParserNodeBase

#---
# Internals
#---

def __check_node_simple(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
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
    return CrupyParserNodeCsvField(
        parent_node = node,
        kind        = 'simple',
        text        = capture,
    )

def __check_node_quoted(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ generic node check """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'lex_text'
    assert node.seq[1].type == 'lex_rep'
    assert node.seq[2].type == 'lex_text'
    capture = ''
    for rep in node.seq[1].rep:
        assert len(rep) == 1
        op = rep[0]
        assert op.type == 'lex_text'
        capture += op.text
    return CrupyParserNodeCsvField(
        parent_node = node,
        kind        = 'quoted',
        text        = capture,
    )

#---
# Public
#---

class CrupyParserNodeCsvField(CrupyParserNodeBase):
    """ CSV field information """
    kind:   str
    text:   str

def csv_parser_prod_field_hook(
    node: CrupyParserNodeBase,
) -> CrupyParserNodeBase:
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
