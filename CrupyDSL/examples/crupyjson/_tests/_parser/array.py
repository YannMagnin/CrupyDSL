"""
crupyjson._tests._parser.array  - `array` production test
"""
__all__ = [
    'json_test_parser_array',
]
from typing import Any

from crupydsl.parser import (
    CrupyParserBase,
    CrupyParserNodeBase,
)

#---
# Internals
#---

def __check_primitive_node(
    node: CrupyParserNodeBase,
    kind: str,
    data: Any,
) -> None:
    """ check primitive node
    """
    assert node.type == 'json_primitive'
    assert node.kind == kind
    assert node.data == data

#---
# Public
#---

def json_test_parser_array(parser: CrupyParserBase) -> None:
    """ test `array` production
    """
    print('-= check array =-')
    print('- primitive (mix)...')
    parser.register_stream(
        '[0,"oui non",true,false,null]'
        '[[0,1,2],[true,null]]'
    )
    node = parser.execute('array')
    assert node is not None
    assert node.type == 'json_array'
    assert len(node.node_list) == 5
    __check_primitive_node(node.node_list[0], 'digit', '0')
    __check_primitive_node(node.node_list[1], 'string', 'oui non')
    __check_primitive_node(node.node_list[2], 'boolean', True)
    __check_primitive_node(node.node_list[3], 'boolean', False)
    __check_primitive_node(node.node_list[4], 'nullable', None)
    print('- container (array)...')
    node = parser.execute('array')
    assert node is not None
    assert node.type == 'json_array'
    assert len(node.node_list) == 2
    assert node.node_list[0].type == 'json_statement'
    assert node.node_list[0].node.type == 'json_container'
    assert node.node_list[0].node.kind == 'json_array'
    array0 = node.node_list[0].node.node
    assert len(array0.node_list) == 3
    __check_primitive_node(array0.node_list[0], 'digit', '0')
    __check_primitive_node(array0.node_list[1], 'digit', '1')
    __check_primitive_node(array0.node_list[2], 'digit', '2')
    assert node.node_list[1].type == 'json_statement'
    assert node.node_list[1].node.type == 'json_container'
    assert node.node_list[1].node.kind == 'json_array'
    array1 = node.node_list[1].node.node
    assert len(array1.node_list) == 2
    __check_primitive_node(array1.node_list[0], 'boolean', True)
    __check_primitive_node(array1.node_list[1], 'nullable', None)
