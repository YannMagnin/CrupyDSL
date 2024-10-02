"""
tests.dsl.dsl - test dsl productions
"""
from crupydsl.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydsl.parser import CrupyDSLParserBaseException

#---
# Public
#---

## fonctional

def test_simple_dsl() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream("<entry> ::= \"yes\" <test>")
    node = CRUPY_DSL_PARSER_OBJ.execute('crupy_dsl')
    assert node.type == 'dsl_entry'
    assert len(node.productions) == 1
    assert node.productions[0].type == 'dsl_production'
    assert node.productions[0].production_name == 'entry'

def test_simple_dsl_with_spaces() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream("""
        <entry> ::= "yes" <test>
    """)
    node = CRUPY_DSL_PARSER_OBJ.execute('crupy_dsl')
    assert node.type == 'dsl_entry'
    assert len(node.productions) == 1
    assert node.productions[0].type == 'dsl_production'
    assert node.productions[0].production_name == 'entry'

def test_multiline_dsl() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream("""
        <entry> ::= "yes" <test>
        <test>  ::= "test"
    """)
    node = CRUPY_DSL_PARSER_OBJ.execute('crupy_dsl')
    assert node.type == 'dsl_entry'
    assert len(node.productions) == 2
    assert node.productions[0].type == 'dsl_production'
    assert node.productions[0].production_name == 'entry'
    assert node.productions[1].type == 'dsl_production'
    assert node.productions[1].production_name == 'test'

## error

def test_error_broken_production() -> None:
    """ test error
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('aaaaaa')
        CRUPY_DSL_PARSER_OBJ.execute('crupy_dsl')
        raise AssertionError('production \'crupy_dsl\' executed')
    except CrupyDSLParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 1\n'
            'aaaaaa\n'
            '^\n'
            'SyntaxError: missing opening chevron'
        )
        assert err.reason == 'missing opening chevron'
