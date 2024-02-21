"""
crupydsl._tests._parser.field   - test parser `field*` productions
"""
__all__ = [
    'csv_test_parser_field',
]

from crupydslparser.core.parser import (
    CrupyParserNode,
    CrupyParserBase,
)


#---
# Internals
#---

## helper

def __check_node_simple(node: CrupyParserNode|None, text: str) -> None:
    """ generic node check """
    try:
        assert node is not None
        assert node['name'] == 'lex_rep'
        assert len(node['rep']) == len(text)
        capture = ''
        for rep in node['rep']:
            assert len(rep) == 1
            op = rep[0]
            assert op['name'] == 'lex_seq'
            assert len(op['seq']) == 1
            assert op['seq'][0]['name'] == 'lex_text'
            capture += op['seq'][0]['text']
        assert capture == text
    except AssertionError:
        print(
            '\033[0;33m'
            f"unable to validate the node '{node}' with '{text}'"
            '\033[0m'
        )

def __check_node_quoted(node: CrupyParserNode|None, text: str) -> None:
    """ generic node check """
    try:
        assert node is not None
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
        print(capture)
        assert capture == text
    except AssertionError:
        print(
            '\033[0;33m'
            f"unable to validate the node '{node}' with '{text}'"
            '\033[0m'
        )

## tests

def _csv_test_parser_field_simple(parser: CrupyParserBase) -> None:
    """ test the `field_simple` production
    """
    print('-= check field simple =-')
    print('> simple success...')
    parser.register_stream('abcd,efgh,ekip667')
    __check_node_simple(parser.execute('field_simple'), 'abcd')
    assert parser.stream.read_char() == ','
    __check_node_simple(parser.execute('field_simple'), 'efgh')
    assert parser.stream.read_char() == ','
    __check_node_simple(parser.execute('field_simple'), 'ekip667')


def _csv_test_parser_field_quoted(parser: CrupyParserBase) -> None:
    """ test the `field_simple` production
    """
    print('-= check field quoted =-')
    print('> simple success...')
    parser.register_stream('"abcd","efgh,oui",",, \t\v oui \vnon"')
    __check_node_quoted(parser.execute('field_quoted'), 'abcd')
    assert parser.stream.read_char() == ','
    __check_node_quoted(parser.execute('field_quoted'), 'efgh,oui')
    assert parser.stream.read_char() == ','
    __check_node_quoted(parser.execute('field_quoted'), ',, \t\v oui \vnon')

#---
# Public
#---

def csv_test_parser_field(parser: CrupyParserBase) -> None:
    """ test `field*` productions
    """
    _csv_test_parser_field_simple(parser)
    _csv_test_parser_field_quoted(parser)
