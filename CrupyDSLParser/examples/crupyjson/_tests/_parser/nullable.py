"""
crupyjson._tests._parser.nullable   - nullable production test
"""
__all__ = [
    'json_test_parser_nullable',
]

from crupydslparser.core.parser import CrupyParserBase

#---
# Public
#---

def json_test_parser_nullable(parser: CrupyParserBase) -> None:
    """ test `nullable` production
    """
    print('-= check nullable =-')
    parser.register_stream('null')
    node = parser.execute('nullable')
    assert node is not None
    assert node['name'] == 'json_nullable'
