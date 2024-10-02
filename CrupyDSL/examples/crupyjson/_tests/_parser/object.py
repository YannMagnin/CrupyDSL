"""
crupyjson._tests._parser.object  - `object` production test
"""
__all__ = [
    'json_test_parser_object',
]

from crupydsl.parser import CrupyParserBase

#---
# Public
#---

def json_test_parser_object(parser: CrupyParserBase) -> None:
    """ test `object` production
    """
    print('-= check object =-')
    print('- primitive...')
    parser.register_stream('{"ekip667":0,"abc def":[0,9]}')
    node = parser.execute('object')
    assert node is not None
    assert node.type == 'json_object'
    assert len(node.members) == 2
    assert node.members[0].type == 'json_member'
    assert node.members[0].key == 'ekip667'
    assert node.members[0].value.type == 'json_primitive'
    assert node.members[0].value.kind == 'digit'
    assert node.members[0].value.data == '0'
    assert node.members[1].type == 'json_member'
    assert node.members[1].key == 'abc def'
    assert node.members[1].value.type == 'json_array'
    assert len(node.members[1].value.node_list) == 2
    array0 = node.members[1].value.node_list
    assert array0[0].type == 'json_primitive'
    assert array0[0].kind == 'digit'
    assert array0[0].data == '0'
    assert array0[1].type == 'json_primitive'
    assert array0[1].kind == 'digit'
    assert array0[1].data == '9'
