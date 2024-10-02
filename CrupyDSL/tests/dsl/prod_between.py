"""
tests.dsl.between - test between production
"""
from crupydsl.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydsl.parser.exception import CrupyDSLParserBaseException

#---
# Public
#---

## valid

def test_simple_success_0() -> None:
    """ valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream(':digit:..."\'"')
    node0 = CRUPY_DSL_PARSER_OBJ.execute('between')
    assert node0.type == 'dsl_between'
    assert node0.kind == 'no_newline'
    assert node0.opening.type == 'dsl_builtin'
    assert node0.closing.type == 'dsl_string'

def test_simple_success_1() -> None:
    """ valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('<test_oui>.!.("aa"|:newline:)')
    node0 = CRUPY_DSL_PARSER_OBJ.execute('between')
    assert node0.type == 'dsl_between'
    assert node0.kind == 'newline'
    assert node0.opening.type == 'dsl_production_name'
    assert node0.closing.type == 'dsl_group'

## error

def test_simple_fail_0() -> None:
    """ invalid case
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('digit:..."\'"')
        CRUPY_DSL_PARSER_OBJ.execute('between')
        raise AssertionError('production executed')
    except CrupyDSLParserBaseException as err:
        assert err.reason == 'unable to validate the opening request'

def test_simple_fail_1() -> None:
    """ invalid case
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('(:digit:|<test>)*.."\'"')
        CRUPY_DSL_PARSER_OBJ.execute('between')
        raise AssertionError('production executed')
    except CrupyDSLParserBaseException as err:
        assert err.reason == (
            'unable to validate the type of between operation '
            'requested'
        )

def test_simple_fail_2() -> None:
    """ invalid case
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('(:digit:|<test>)*.!."\'')
        CRUPY_DSL_PARSER_OBJ.execute('between')
        raise AssertionError('production executed')
    except CrupyDSLParserBaseException as err:
        assert err.reason == 'unable to validate the enclosing request'
