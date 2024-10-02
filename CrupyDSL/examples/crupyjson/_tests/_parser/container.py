"""
crupyjson._tests._parser.container  - `container` production test
"""
__all__ = [
    'json_test_parser_container',
]

from crupydsl.parser import CrupyDSLParserBase

#---
# Public
#---

def json_test_parser_container(parser: CrupyDSLParserBase) -> None:
    """ test `container` production
    """
    print('-= check container =-')
    print('- array...')
    parser.register_stream('[0,"oui"]{"abc":0}')
    node = parser.execute('container')
    assert node is not None
    assert node.type == 'json_container'
    assert node.node.type == 'json_array'
    array = node.node
    assert len(array.node_list) == 2
    assert array.node_list[0].type == 'json_primitive'
    assert array.node_list[0].kind == 'digit'
    assert array.node_list[0].data == '0'
    assert array.node_list[1].type == 'json_primitive'
    assert array.node_list[1].kind == 'string'
    assert array.node_list[1].data == 'oui'
    print('- object...')
    node = parser.execute('container')
    assert node is not None
    assert node.type == 'json_container'
    assert node.node.type == 'json_object'
    obj = node.node
    assert len(obj.members) == 1
    assert obj.members[0].type == 'json_member'
    assert obj.members[0].key == 'abc'
    assert obj.members[0].value.type == 'json_primitive'
    assert obj.members[0].value.kind == 'digit'
    assert obj.members[0].value.data == '0'
