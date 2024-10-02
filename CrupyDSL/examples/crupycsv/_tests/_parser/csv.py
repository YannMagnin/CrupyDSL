"""
crupycsv._tests._parser.csv     - full CSV tests
"""
__all__ = [
    'csv_test_parser_csv',
]

from crupydsl.parser import (
    CrupyDSLParserBase,
    CrupyDSLParserNodeBase,
)

#---
# Internals
#---

def __check_record0(record: CrupyDSLParserNodeBase) -> None:
    """ check the first line
    """
    assert len(record.fields) == 5
    for i, field in enumerate(record.fields):
        assert field.type == 'csv_field'
        if i == 0:
            assert field.kind == 'simple'
            assert field.text == 'abcd'
        if i == 1:
            assert field.kind == 'quoted'
            assert field.text == 'efgh,oui'
        if i == 2:
            assert field.kind == 'quoted'
            assert field.text == ',, \t oui non'
        if i == 3:
            assert field.kind == 'simple'
            assert field.text == ''
        if i == 4:
            assert field.kind == 'simple'
            assert field.text == 'qwerty'


def __check_record1(record: CrupyDSLParserNodeBase) -> None:
    """ check the second line
    """
    assert len(record.fields) == 2
    assert record.fields[0].type == 'csv_field'
    assert record.fields[0].kind == 'quoted'
    assert record.fields[0].text == 'ekip667'
    assert record.fields[1].type == 'csv_field'
    assert record.fields[1].kind == 'simple'
    assert record.fields[1].text == 'oui'

def __check_record2(record: CrupyDSLParserNodeBase) -> None:
    """ check the third line
    """
    assert len(record.fields) == 1
    assert record.fields[0].type == 'csv_field'
    assert record.fields[0].kind == 'simple'
    assert record.fields[0].text == 'abcdef'

#---
# Public
#---

def csv_test_parser_csv(parser: CrupyDSLParserBase) -> None:
    """ test `csv` production
    """
    print('-= production `csv` tests =-')
    parser.register_stream(
        'abcd,"efgh,oui",",, \t oui non",,qwerty\n'
        '"ekip667",oui\n'
        'abcdef\n'
    )
    node = parser.execute('csv')
    assert node is not None
    assert node.type == 'csv'
    assert len(node.records) == 3
    for i, record in enumerate(node.records):
        assert record.type == 'csv_record'
        (
            __check_record0,
            __check_record1,
            __check_record2,
        )[i](record)
