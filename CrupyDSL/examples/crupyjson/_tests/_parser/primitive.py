"""
crupyjson._tests._parser.primitive  - `primitive` production test
"""
__all__ = [
    'json_test_parser_primitive',
]

from crupydsl.parser import CrupyDSLParserBase

#---
# Public
#---

def json_test_parser_primitive(parser: CrupyDSLParserBase) -> None:
    """ test `primitive` production
    """
    print('-= check primitive =-')
    print('- digit')
    parser.register_stream('0"aaaa"\'oui non test\'truefalsenull')
    node = parser.execute('primitive')
    assert node is not None
    assert node.type == 'json_primitive'
    assert node.kind == 'digit'
    assert node.data == '0'
    print('- string (single)...')
    node = parser.execute('primitive')
    assert node is not None
    assert node.type == 'json_primitive'
    assert node.kind == 'string'
    assert node.data == 'aaaa'
    print('- string (double)...')
    node = parser.execute('primitive')
    assert node is not None
    assert node.type == 'json_primitive'
    assert node.kind == 'string'
    assert node.data == 'oui non test'
    print('- boolean (true)...')
    node = parser.execute('primitive')
    assert node is not None
    assert node.type == 'json_primitive'
    assert node.kind == 'boolean'
    assert node.data is True
    print('- boolean (false)...')
    node = parser.execute('primitive')
    assert node is not None
    assert node.type == 'json_primitive'
    assert node.kind == 'boolean'
    assert node.data is False
    print('- nullable...')
    node = parser.execute('primitive')
    assert node is not None
    assert node.type == 'json_primitive'
    assert node.kind == 'nullable'
    assert node.data is None
