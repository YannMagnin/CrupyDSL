"""
tests.lexer.dsl_production_name - test `crupy_dsl_production_name` rule
"""
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.parser._lexer import CrupyDSLLexerOpProductionCall
from crupydsl.grammar._dsl import (
    CRUPY_DSL_PARSER_OBJ,
    dsl_compil_grammar_node,
)

# allow access private members to ensure that the DSL node translation has
# been correctly done
# pylint: disable=locally-disabled,W0212

#---
# Public
#---

def test_simple_success() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('<oui_non><abcd><qwer_')
    node1 = CRUPY_DSL_PARSER_OBJ.execute('production_name')
    node2 = CRUPY_DSL_PARSER_OBJ.execute('production_name')
    assert node1.type == 'dsl_production_name'
    assert node2.type == 'dsl_production_name'
    assert node1.production_name == 'oui_non'
    assert node2.production_name == 'abcd'
    operation = dsl_compil_grammar_node(node1)
    assert isinstance(operation, CrupyDSLLexerOpProductionCall)
    assert operation._production_name == 'oui_non'
    operation = dsl_compil_grammar_node(node2)
    assert isinstance(operation, CrupyDSLLexerOpProductionCall)
    assert operation._production_name == 'abcd'

def test_error_start() -> None:
    """ error test
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('oui_non>')
        CRUPY_DSL_PARSER_OBJ.execute('production_name')
        raise AssertionError('production \'production_name\' executed')
    except CrupyDSLParserBaseException as err:
        assert err.reason == 'missing opening chevron'

def test_error_content() -> None:
    """ error test
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('<9->')
        CRUPY_DSL_PARSER_OBJ.execute('production_name')
        raise AssertionError('production \'production_name\' executed')
    except CrupyDSLParserBaseException as err:
        assert err.reason == (
            'production name should only contain alphanumerical and '
            'underscore characters'
        )

def test_error_close() -> None:
    """ error test
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('<oui_non')
        CRUPY_DSL_PARSER_OBJ.execute('production_name')
        raise AssertionError('production \'production_name\' executed')
    except CrupyDSLParserBaseException as err:
        assert err.reason == 'missing enclosing chevron'
