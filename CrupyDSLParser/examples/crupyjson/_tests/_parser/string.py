"""
crupyjson._tests._parser.string    - string production test
"""
__all__ = [
    'json_test_parser_string',
]

from crupydslparser.core.parser import CrupyParserBase

#---
# Public
#---

def json_test_parser_string(parser: CrupyParserBase) -> None:
    """ test `string` production
    """
    print('-= check string =-')
    print('- check double quote...')
    parser.register_stream('"667 oui ~# \\ dslk"')
    node = parser.execute('string')
    assert node is not None
    assert node['name'] == 'json_string'
    assert node['text'] == '667 oui ~# \\ dslk'
    print('- check single quote...')
    parser.register_stream('\'667 oui ~# \\\tdslk\'')
    node = parser.execute('string')
    assert node is not None
    assert node['name'] == 'json_string'
    assert node['text'] == '667 oui ~# \\\tdslk'
