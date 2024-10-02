"""
crupyjson._tests._parser.member  - `member` production test
"""
__all__ = [
    'json_test_parser_member',
]

from crupydsl.parser import CrupyParserBase

#---
# Public
#---

def json_test_parser_member(parser: CrupyParserBase) -> None:
    """ test `member` production
    """
    print('-= check member =-')
    print('- primitive...')
    parser.register_stream('"ekip667":0')
    node = parser.execute('member')
    assert node is not None
    assert node.type == 'json_member'
    assert node.key == 'ekip667'
    assert node.value.type == 'json_primitive'
    assert node.value.kind == 'digit'
    assert node.value.data == '0'
