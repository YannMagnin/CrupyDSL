"""
tests.dsl.builtin - test builtin production
"""
from crupydsl.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydsl.parser.exception import CrupyDSLParserBaseException

#---
# Public
#---

def test_simple_success() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream(':digit::any:')
    node0 = CRUPY_DSL_PARSER_OBJ.execute('builtin')
    node1 = CRUPY_DSL_PARSER_OBJ.execute('builtin')
    assert node0.type == 'dsl_builtin'
    assert node0.kind == 'digit'
    assert node1.type == 'dsl_builtin'
    assert node1.kind == 'any'

def test_error_start() -> None:
    """ test error
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('digit:')
        CRUPY_DSL_PARSER_OBJ.execute('builtin')
    except CrupyDSLParserBaseException as err:
        assert err.reason == 'missing starting colon'

def test_error_context() -> None:
    """ test error
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('::')
        CRUPY_DSL_PARSER_OBJ.execute('builtin')
    except CrupyDSLParserBaseException as err:
        assert err.reason == 'missing builtin name'

def test_error_end() -> None:
    """ test error
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream(':builtin')
        CRUPY_DSL_PARSER_OBJ.execute('builtin')
    except CrupyDSLParserBaseException as err:
        assert err.reason == 'missing enclosing colon'
