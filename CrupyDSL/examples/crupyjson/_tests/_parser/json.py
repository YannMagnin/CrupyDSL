"""
crupyjson._tests._parser.json    - boolean production test
"""
__all__ = [
    'json_test_parser_json',
]

from crupydsl.parser import CrupyParserBase

#---
# Public
#---

def json_test_parser_json(parser: CrupyParserBase) -> None:
    """ test `json` production
    """
    print('-= check json =-')
    print('- check primitive...')
    parser.register_stream('0')
    node = parser.execute('json')
    assert node is not None
    assert node.type == 'json_statement'
    assert node.node.type == 'json_primitive'
    assert node.node.kind == 'digit'
    assert node.node.data == '0'
    print('- check container...')
    parser.register_stream('[1,2]')
    node = parser.execute('json')
    assert node is not None
    assert node.type == 'json_statement'
    assert node.node.type == 'json_container'
    assert node.node.node.type == 'json_array'
