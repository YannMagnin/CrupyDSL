"""
crupycsv._tests._parser.record  - CSV `record` production test
"""
__all__ = [
    'csv_test_parser_record',
]

from crupydslparser.core.parser import CrupyParserBase

#---
# Public
#---

def csv_test_parser_record(parser: CrupyParserBase) -> None:
    """ test `record` production
    """
    print('-= check mixed field =-')
    parser.register_stream('abcd,"efgh,oui",",, \t\v oui \vnon",,qwerty')
    node = parser.execute('record')
    assert node is not None
    assert node['name'] == 'csv_record'
    assert len(node['fields']) == 5
    for i, field in enumerate(node['fields']):
        assert field['name'] == 'csv_field'
        if i == 0:
            assert field['kind'] == 'simple'
            assert field['text'] == 'abcd'
        if i == 1:
            assert field['kind'] == 'quoted'
            assert field['text'] == 'efgh,oui'
        if i == 2:
            assert field['kind'] == 'quoted'
            assert field['text'] == ',, \t\v oui \vnon'
        if i == 3:
            assert field['kind'] == 'simple'
            assert field['text'] == ''
        if i == 4:
            assert field['kind'] == 'simple'
            assert field['text'] == 'qwerty'
