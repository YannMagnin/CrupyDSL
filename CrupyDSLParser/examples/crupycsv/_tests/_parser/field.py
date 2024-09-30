"""
crupydsl._tests._parser.field   - test parser `field*` productions
"""
__all__ = [
    'csv_test_parser_field',
]
from typing import Union

from crupydslparser.parser import (
    CrupyParserNodeBase,
    CrupyParserBase,
)

#---
# Internals
#---

## helper

def __check_node_simple(
    node: Union[CrupyParserNodeBase,None],
    text: str,
) -> None:
    """ generic node check """
    try:
        assert node is not None
        assert node.type == 'lex_rep'
        assert len(node.rep) == len(text)
        capture = ''
        for rep in node.rep:
            assert len(rep) == 1
            op = rep[0]
            assert op.type == 'lex_seq'
            assert len(op.seq) == 1
            assert op.seq[0].type == 'lex_text'
            capture += op.seq[0].text
        assert capture == text
    except AssertionError:
        print(
            '\033[0;33m'
            f"unable to validate the node '{node}' with '{text}'"
            '\033[0m'
        )

def __check_node_quoted(
    node: Union[CrupyParserNodeBase,None],
    text: str,
) -> None:
    """ generic node check """
    try:
        assert node is not None
        assert node.type == 'lex_between'
        assert node.captured_start.type == 'lex_text'
        assert node.captured_end.type == 'lex_text'
        assert node.captured_middle == text
    except AssertionError:
        print(
            '\033[0;33m'
            f"unable to validate the node '{node}' with '{text}'"
            '\033[0m'
        )

def __check_node_mixed(
    node: Union[CrupyParserNodeBase,None],
    text: str,
    kind: str,
) -> None:
    """ check real field information
    """
    try:
        assert node is not None
        assert node.type == 'csv_field'
        assert node.kind == kind
        assert node.text == text
    except AssertionError:
        print(
            '\033[0;33m'
            f"unable to validate the mixed node '{node}' with "
            f"'{kind}:{text}'"
            '\033[0m'
        )

## tests

def _csv_test_parser_field_simple(parser: CrupyParserBase) -> None:
    """ test the `field_simple` production
    """
    print('- check field simple...')
    parser.register_stream('abcd,efgh,ekip667')
    __check_node_simple(parser.execute('field_simple'), 'abcd')
    with parser.stream as context:
        assert context.read_char() == ','
        context.validate()
    __check_node_simple(parser.execute('field_simple'), 'efgh')
    with parser.stream as context:
        assert context.read_char() == ','
        context.validate()
    __check_node_simple(parser.execute('field_simple'), 'ekip667')


def _csv_test_parser_field_quoted(parser: CrupyParserBase) -> None:
    """ test the `field_simple` production
    """
    print('- check field quoted...')
    parser.register_stream('"abcd","efgh,oui",",, \t oui non"')
    __check_node_quoted(parser.execute('field_quoted'), 'abcd')
    with parser.stream as context:
        assert context.read_char() == ','
        context.validate()
    __check_node_quoted(parser.execute('field_quoted'), 'efgh,oui')
    with parser.stream as context:
        assert context.read_char() == ','
        context.validate()
    __check_node_quoted(
        parser.execute('field_quoted'),
        ',, \t oui non',
    )

def _csv_test_parser_field_mixed(parser: CrupyParserBase) -> None:
    """ test the `field` production
    """
    print('- mixed node...')
    parser.register_stream('abcd,"efgh,oui",",, \t oui non",,qwerty')
    __check_node_mixed(parser.execute('field'), 'abcd', 'simple')
    with parser.stream as context:
        assert context.read_char() == ','
        context.validate()
    __check_node_mixed(parser.execute('field'), 'efgh,oui', 'quoted')
    with parser.stream as context:
        assert context.read_char() == ','
        context.validate()
    __check_node_mixed(
        parser.execute('field'),
        ',, \t oui non',
        'quoted',
    )
    with parser.stream as context:
        assert context.read_char() == ','
        context.validate()
    __check_node_mixed(parser.execute('field'), '', 'simple')
    with parser.stream as context:
        assert context.read_char() == ','
        context.validate()
    __check_node_mixed(parser.execute('field'), 'qwerty', 'simple')

#---
# Public
#---

def csv_test_parser_field(parser: CrupyParserBase) -> None:
    """ test `field*` productions
    """
    print('-= production `field` tests =-')
    _csv_test_parser_field_simple(parser)
    _csv_test_parser_field_quoted(parser)
    _csv_test_parser_field_mixed(parser)
