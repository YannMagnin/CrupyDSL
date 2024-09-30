"""
tests.dsl.error - test error productions
"""
from crupydslparser.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

## fonctional

def test_error() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('@error("salut a tous")')
    node = CRUPY_DSL_PARSER_OBJ.execute('error')
    assert node.type == 'dsl_error'
    assert node.kind == 'error'
    assert node.error_name == 'salut a tous'

def test_error_hook() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('@error_hook("salut a tous")')
    node = CRUPY_DSL_PARSER_OBJ.execute('error')
    assert node.type == 'dsl_error'
    assert node.kind == 'hook'
    assert node.error_name == 'salut a tous'

## error

def test_broken_start() -> None:
    """ error test
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('error("salut a tous")')
        CRUPY_DSL_PARSER_OBJ.execute('error')
        raise AssertionError('production \'error\' execute')
    except CrupyParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 1\n'
            'error("salut a tous")\n'
            '^\n'
            'SyntaxError: manual error must start with "@"'
        )
        assert err.reason == 'manual error must start with "@"'

def test_broken_kind() -> None:
    """ error test
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('@aaerror_foo("salut a tous")')
        CRUPY_DSL_PARSER_OBJ.execute('error')
        raise AssertionError('production \'error\' execute')
    except CrupyParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 2\n'
            '@aaerror_foo("salut a tous")\n'
            '~^\n'
            'SyntaxError: only \'error\' and \'error_hook\' are '
            'currently supported'
        )
        assert err.reason == (
            'only \'error\' and \'error_hook\' are currently supported'
        )

def test_broken_openp() -> None:
    """ error test
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('@error"salut a tous")')
        CRUPY_DSL_PARSER_OBJ.execute('error')
        raise AssertionError('production \'error\' execute')
    except CrupyParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 7\n'
            '@error"salut a tous")\n'
            '~~~~~~^\n'
            'SyntaxError: missing opening parenthesis'
        )
        assert err.reason == 'missing opening parenthesis'

def test_broken_closep() -> None:
    """ error test
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('@error("salut a tous"')
        CRUPY_DSL_PARSER_OBJ.execute('error')
        raise AssertionError('production \'error\' execute')
    except CrupyParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 22\n'
            '@error("salut a tous"\n'
            '~~~~~~~~~~~~~~~~~~~~~^\n'
            'SyntaxError: missing enclosing parenthesis'
        )
        assert err.reason == 'missing enclosing parenthesis'
