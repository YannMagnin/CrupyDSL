"""
tests.dsl.production - test production productions
"""
from crupydsl.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydsl.parser.exception import CrupyDSLParserBaseException

#---
# Public
#---

def test_simple_test() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('<entry> ::= "allo?"')
    node = CRUPY_DSL_PARSER_OBJ.execute('production')
    assert node.type == 'dsl_production'
    assert node.production_name == 'entry'
    assert node.statement.type == 'dsl_statement'
    assert len(node.statement.alternatives) == 1

def test_simple_test_with_space() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream("""
        <entry> ::= "allo?"
    """)
    node = CRUPY_DSL_PARSER_OBJ.execute('production')
    assert node.type == 'dsl_production'
    assert node.production_name == 'entry'
    assert node.statement.type == 'dsl_statement'
    assert len(node.statement.alternatives) == 1

def test_multiple_production() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream("""
        <entry> ::= "allo?" <oui>
        <oui>   ::= "non"
    """)
    node = CRUPY_DSL_PARSER_OBJ.execute('production')
    assert node.type == 'dsl_production'
    assert node.production_name == 'entry'
    assert node.statement.type == 'dsl_statement'
    assert len(node.statement.alternatives) == 1
    node = CRUPY_DSL_PARSER_OBJ.execute('production')
    assert node.type == 'dsl_production'
    assert node.production_name == 'oui'
    assert node.statement.type == 'dsl_statement'
    assert len(node.statement.alternatives) == 1

## error

def test_error_prodname() -> None:
    """ test error
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('<entry ::= "allo?"')
        CRUPY_DSL_PARSER_OBJ.execute('production')
        raise AssertionError('production \'production\' executed')
    except CrupyDSLParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 7\n'
            '<entry ::= "allo?"\n'
            '~~~~~~^\n'
            'SyntaxError: missing enclosing chevron'
        )
        assert err.reason == 'missing enclosing chevron'

def test_error_space0() -> None:
    """ test error
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('<entry>::= "allo?"')
        CRUPY_DSL_PARSER_OBJ.execute('production')
        raise AssertionError('production \'production\' executed')
    except CrupyDSLParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 8\n'
            '<entry>::= "allo?"\n'
            '~~~~~~~^\n'
            'SyntaxError: missing space between production name and '
            'equal sign'
        )
        assert err.reason == (
            'missing space between production name and equal sign'
        )

def test_error_space1() -> None:
    """ test error
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('<entry> ::="allo?"')
        CRUPY_DSL_PARSER_OBJ.execute('production')
        raise AssertionError('production \'production\' executed')
    except CrupyDSLParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 12\n'
            '<entry> ::="allo?"\n'
            '~~~~~~~~~~~^\n'
            'SyntaxError: missing space between equal sign and statement'
        )
        assert err.reason == (
            'missing space between equal sign and statement'
        )

def test_error_statement() -> None:
    """ test error
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('<entry> ::= "allo?')
        CRUPY_DSL_PARSER_OBJ.execute('production')
        raise AssertionError('production \'production\' executed')
    except CrupyDSLParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 19\n'
            '<entry> ::= "allo?\n'
            '            ~~~~~~^\n'
            'SyntaxError: missing enclosing quote'
        )
        assert err.reason == 'missing enclosing quote'

def test_error_eol() -> None:
    """ test error
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('<entry> ::= "allo?" ::=')
        CRUPY_DSL_PARSER_OBJ.execute('production')
        raise AssertionError('production \'production\' executed')
    except CrupyDSLParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 20\n'
            '<entry> ::= "allo?" ::=\n'
            '~~~~~~~~~~~~~~~~~~~^\n'
            'SyntaxError: missing an end-of-line or and end-of-file '
            'to validate the production'
        )
        assert err.reason == (
            'missing an end-of-line or and end-of-file to validate '
            'the production'
        )
