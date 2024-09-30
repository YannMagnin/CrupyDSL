"""
tests.dsl.end_of_line   - test productions
"""
from crupydslparser.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

def test_simple_newline() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('\n')
    node = CRUPY_DSL_PARSER_OBJ.execute('eol')
    assert node.type == 'dsl_eol'

def test_complexe_newline() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('\r\n')
    node = CRUPY_DSL_PARSER_OBJ.execute('eol')
    assert node.type == 'dsl_eol'

def test_error() -> None:
    """ simple valid case
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('prout')
        CRUPY_DSL_PARSER_OBJ.execute('eol')
        raise AssertionError('production eol has been executed')
    except CrupyParserBaseException as err:
        assert err.reason == 'not an end-of-file'
