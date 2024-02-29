"""
crupyjson._tests._parser.statement    - boolean production test
"""
__all__ = [
    'json_test_parser_statement',
]

from crupydslparser.core.parser import CrupyParserBase

#---
# Public
#---

def json_test_parser_statement(parser: CrupyParserBase) -> None:
    """ test `statement` production
    """
    print('-= check statement =-')
    print('- check primitive...')
    parser.register_stream('0[1,2]')
    node = parser.execute('statement')
    assert node is not None
    assert node['name'] == 'json_statement'
    assert node['node']['name'] == 'json_primitive'
    assert node['node']['kind'] == 'digit'
    assert node['node']['data'] == '0'
    print('- check container...')
    node = parser.execute('statement')
    assert node is not None
    assert node['name'] == 'json_statement'
    assert node['node']['name'] == 'json_container'
    assert node['node']['node']['name'] == 'json_array'
