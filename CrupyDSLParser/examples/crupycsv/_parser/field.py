"""
crupydslparser.core._parser.field   - `field` production definition
"""
__all__ = [
    'csv_parser_prod_field_hook',
]

from crupydslparser.core.parser import (
    CrupyParserNode,
    CrupyParserException,
)

#---
# Internals
#---

def __check_node_simple(node: CrupyParserNode) -> CrupyParserNode|None:
    """ field simple node check
    """
    if node['name'] != 'lex_rep':
        return None
    try:
        capture = ''
        for rep in node['rep']:
            assert len(rep) == 1
            op = rep[0]
            assert op['name'] == 'lex_seq'
            assert len(op['seq']) == 1
            assert op['seq'][0]['name'] == 'lex_text'
            capture += op['seq'][0]['text']
        return CrupyParserNodeCsvField(
            parent_node = node,
            kind        = 'simple',
            text        = capture,
        )
    except AssertionError as err:
        raise CrupyParserException(
            f"unable to validate the `field_simple` node '{node}'"
        ) from err

def __check_node_quoted(node: CrupyParserNode) -> CrupyParserNode|None:
    """ generic node check """
    if node['name'] != 'lex_seq':
        return None
    try:
        assert len(node['seq']) == 3
        assert node['seq'][0]['name'] == 'lex_text'
        assert node['seq'][1]['name'] == 'lex_rep'
        assert node['seq'][2]['name'] == 'lex_text'
        capture = ''
        for rep in node['seq'][1]['rep']:
            assert len(rep) == 1
            op = rep[0]
            assert op['name'] == 'lex_text'
            capture += op['text']
        return CrupyParserNodeCsvField(
            parent_node = node,
            kind        = 'quoted',
            text        = capture,
        )
    except AssertionError as err:
        raise CrupyParserException(
            f"unable to validate the `field_quoted` node '{node}'"
        ) from err

#---
# Public
#---

class CrupyParserNodeCsvField(CrupyParserNode):
    """ CSV field information """
    kind:   str
    text:   str

def csv_parser_prod_field_hook(node: CrupyParserNode) -> CrupyParserNode:
    """ generate more appropriate node concerning `field` output

    @note
    - field        ::= <quoted_content> | <simple_content>
    - field_quoted ::= "\"" (<letter>|<digit>|<symbol>|<space>)+ "\""
    - field_simple ::= ((?!,)(<letter>|<digit>|<symbol>))*
    """
    if (new_node := __check_node_simple(node)):
        return new_node
    if (new_node := __check_node_quoted(node)):
        return new_node
    raise CrupyParserException(
        f"Unrecognised CSV `field` node ({node})"
    )
