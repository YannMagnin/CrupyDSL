"""
crupyjson._tests._parser.boolean    - boolean production test
"""
__all__ = [
    'json_test_parser_boolean',
]

from crupydslparser.core.parser import CrupyParserBase

#---
# Public
#---

def json_test_parser_boolean(parser: CrupyParserBase) -> None:
    """ test `boolean` production
    """
    print('-= check boolean =-')
    print('- check true...')
    parser.register_stream('true')
    node = parser.execute('boolean')
    assert node is not None
    assert node.type == 'json_boolean'
    assert node.state is True
    print('- check false...')
    parser.register_stream('false')
    node = parser.execute('boolean')
    assert node is not None
    assert node.type == 'json_boolean'
    assert node.state is False
