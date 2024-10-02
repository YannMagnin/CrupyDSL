"""
crupyjson._tests._parser.statement    - boolean production test
"""
__all__ = [
    'json_test_parser_statement',
]

from crupydsl.parser import CrupyDSLParserBase

#---
# Public
#---

def json_test_parser_statement(parser: CrupyDSLParserBase) -> None:
    """ test `statement` production
    """
    print('-= check statement =-')
    print('- check primitive...')
    parser.register_stream('0[1,2]')
    node = parser.execute('statement')
    assert node is not None
    assert node.type == 'json_statement'
    assert node.node.type == 'json_primitive'
    assert node.node.kind == 'digit'
    assert node.node.data == '0'
    print('- check container...')
    node = parser.execute('statement')
    assert node is not None
    assert node.type == 'json_statement'
    assert node.node.type == 'json_container'
    assert node.node.node.type == 'json_array'
