"""
crupyjson._tests._parser.nullable   - nullable production test
"""
__all__ = [
    'json_test_parser_nullable',
]

from crupydsl.parser import CrupyDSLParserBase

#---
# Public
#---

def json_test_parser_nullable(parser: CrupyDSLParserBase) -> None:
    """ test `nullable` production
    """
    print('-= check nullable =-')
    parser.register_stream('null')
    node = parser.execute('nullable')
    assert node is not None
    assert node.type == 'json_nullable'
