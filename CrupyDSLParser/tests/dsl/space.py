"""
tests.dsl.space - test space productions
"""
from crupydslparser.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydslparser.parser import CrupyParserBaseException

#---
# Public
#---

## __space

def test_space_lowlevel() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream(' \t \\\n')
    node1 = CRUPY_DSL_PARSER_OBJ.execute('__space')
    node2 = CRUPY_DSL_PARSER_OBJ.execute('__space')
    node3 = CRUPY_DSL_PARSER_OBJ.execute('__space')
    node4 = CRUPY_DSL_PARSER_OBJ.execute('__space')
    assert node1.type == 'dsl_space'
    assert node2.type == 'dsl_space'
    assert node3.type == 'dsl_space'
    assert node4.type == 'dsl_space'

def test_space_lowlevel_error() -> None:
    """ __space lowlevel error
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('q\t \\\na')
        CRUPY_DSL_PARSER_OBJ.execute('__space')
        raise AssertionError('production __space has been executed')
    except CrupyParserBaseException as err:
        assert err.reason == 'not a space'

## space

def test_space() -> None:
    """ space rule
    """
    CRUPY_DSL_PARSER_OBJ.register_stream(' \t \\\na')
    assert CRUPY_DSL_PARSER_OBJ.execute('space') is not None
    with CRUPY_DSL_PARSER_OBJ.stream as context:
        assert context.read_char() == 'a'

def test_space_error() -> None:
    """ space lowlevel error
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('q\t \\\na')
        CRUPY_DSL_PARSER_OBJ.execute('space')
        raise AssertionError('production space has been executed')
    except CrupyParserBaseException as err:
        assert err.reason == 'missing at least one space'

## space_opt

def test_spaceopt_eof() -> None:
    """ space rule
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('a')
    with CRUPY_DSL_PARSER_OBJ.stream as context:
        context.read_char()
        context.validate()
    CRUPY_DSL_PARSER_OBJ.execute('space_opt')

def test_spaceopt_text() -> None:
    """ space rule
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('aa')
    CRUPY_DSL_PARSER_OBJ.execute('space_opt')
