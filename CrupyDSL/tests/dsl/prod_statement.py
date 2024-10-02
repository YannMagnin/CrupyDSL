"""
tests.dsl.statement - test statement productions
"""
from crupydsl.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydsl.parser.exception import CrupyParserBaseException

#---
# Public
#---

## fonctional

def test_prodname() -> None:
    """ test """
    CRUPY_DSL_PARSER_OBJ.register_stream('<test_oui>')
    node = CRUPY_DSL_PARSER_OBJ.execute('statement')
    assert node.type == 'dsl_statement'

def test_one_line() -> None:
    """ simple valid case """
    CRUPY_DSL_PARSER_OBJ.register_stream(
        '<test_oui> | "coucou" | :any: <ekip>\n'
    )
    node = CRUPY_DSL_PARSER_OBJ.execute('statement')
    assert node.type == 'dsl_statement'
    assert len(node.alternatives) == 3
    alts = node.alternatives
    assert alts[0].type == 'dsl_alternative'
    assert alts[1].type == 'dsl_alternative'
    assert alts[2].type == 'dsl_alternative'
    assert len(alts[0].seq) == 1
    assert len(alts[1].seq) == 1
    assert len(alts[2].seq) == 2
    assert alts[0].seq[0].type == 'dsl_production_name'
    assert alts[1].seq[0].type == 'dsl_string'
    assert alts[2].seq[0].type == 'dsl_builtin'
    assert alts[2].seq[1].type == 'dsl_production_name'

def test_multiple_line() -> None:
    """ test multiple line """
    CRUPY_DSL_PARSER_OBJ.register_stream(r""" \
        | <test_oui> \
        | "coucou" \
        | :any: <coucou>
    """)
    node = CRUPY_DSL_PARSER_OBJ.execute('statement')
    assert node.type == 'dsl_statement'
    assert len(node.alternatives) == 3
    alts = node.alternatives
    assert alts[0].type == 'dsl_alternative'
    assert alts[1].type == 'dsl_alternative'
    assert alts[2].type == 'dsl_alternative'
    assert len(alts[0].seq) == 1
    assert len(alts[1].seq) == 1
    assert len(alts[2].seq) == 2
    assert alts[0].seq[0].type == 'dsl_production_name'
    assert alts[1].seq[0].type == 'dsl_string'
    assert alts[2].seq[0].type == 'dsl_builtin'
    assert alts[2].seq[1].type == 'dsl_production_name'

## error

def test_error_broken_alternative() -> None:
    """ test error """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('"yes no maybe')
        CRUPY_DSL_PARSER_OBJ.execute('statement')
        raise AssertionError('production \'statement\' executed')
    except CrupyParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 14\n'
            '"yes no maybe\n'
            '~~~~~~~~~~~~~^\n'
            'SyntaxError: missing enclosing quote'
        )
        assert err.reason == 'missing enclosing quote'
