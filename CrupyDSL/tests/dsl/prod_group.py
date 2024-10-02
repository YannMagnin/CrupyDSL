"""
tests.dsl.group - test group productions
"""
from crupydsl.grammar._dsl._parser import (
    CRUPY_DSL_PARSER_OBJ,
    CrupyDslParserException,
)

#---
# Public
#---

## success

def test_simple() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('(<test_oui>)')
    node = CRUPY_DSL_PARSER_OBJ.execute('group')
    assert node.type == 'dsl_group'
    assert node.lookahead is None
    assert node.operation is None
    assert node.statement.type == 'dsl_statement'
    assert len(node.statement.alternatives) == 1

def test_simple_group() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('(<test_oui> "non")')
    node = CRUPY_DSL_PARSER_OBJ.execute('group')
    assert node.type == 'dsl_group'
    assert node.lookahead is None
    assert node.operation is None
    assert node.statement.type == 'dsl_statement'
    assert len(node.statement.alternatives) == 1

def test_group_lookahead_negative() -> None:
    """ lookahead tests
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('(?!"oui")')
    node = CRUPY_DSL_PARSER_OBJ.execute('group')
    assert node.type == 'dsl_group'
    assert node.lookahead == 'negative'
    assert node.operation is None
    assert node.statement.type == 'dsl_statement'
    assert len(node.statement.alternatives) == 1

def test_group_lookahead_positive() -> None:
    """ lookahead tests
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('(?=<space_opt>)')
    node = CRUPY_DSL_PARSER_OBJ.execute('group')
    assert node.type == 'dsl_group'
    assert node.lookahead == 'positive'
    assert node.operation is None
    assert node.statement.type == 'dsl_statement'
    assert len(node.statement.alternatives) == 1

def test_group_operation_zero_plus() -> None:
    """ operation zero plus
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('(<space_opt> :any:)*')
    node = CRUPY_DSL_PARSER_OBJ.execute('group')
    assert node.type == 'dsl_group'
    assert node.lookahead is None
    assert node.operation == 'zero_plus'
    assert node.statement.type == 'dsl_statement'
    assert len(node.statement.alternatives) == 1

def test_group_operation_one_plus() -> None:
    """ operation one plus
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('(:any: | "2617")+')
    node = CRUPY_DSL_PARSER_OBJ.execute('group')
    assert node.type == 'dsl_group'
    assert node.lookahead is None
    assert node.operation == 'one_plus'
    assert node.statement.type == 'dsl_statement'
    assert len(node.statement.alternatives) == 2

def test_group_operation_optional() -> None:
    """ operation optional
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('(:any: | "2617" <rte>)?')
    node = CRUPY_DSL_PARSER_OBJ.execute('group')
    assert node.type == 'dsl_group'
    assert node.lookahead is None
    assert node.operation == 'optional'
    assert node.statement.type == 'dsl_statement'
    assert len(node.statement.alternatives) == 2

## error

def test_error_start() -> None:
    """ error test """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('oui_non)')
        CRUPY_DSL_PARSER_OBJ.execute('group')
        raise AssertionError('production \'group\' executed')
    except CrupyDslParserException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 1\n'
            'oui_non)\n'
            '^\n'
            'SyntaxError: missing opening parenthesis'
        )
        assert err.reason == 'missing opening parenthesis'

def test_error_close() -> None:
    """ error test
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('(:space:')
        CRUPY_DSL_PARSER_OBJ.execute('group')
        raise AssertionError('production \'group\' executed')
    except CrupyDslParserException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 9\n'
            '(:space:\n'
            '~~~~~~~~^\n'
            'SyntaxError: missing enclosing parenthesis'
        )
        assert err.reason == 'missing enclosing parenthesis'

# @note
# > Since we use the CrupyLexerOpOptional() to fetch group operation,
#   we cannot catch the CrupyLexerOpError() because it will be ignored
#   by the optional behaviour
#
#def test_error_broken_operation(self) -> None:
#    """ error test """
#    try:
#        CRUPY_DSL_PARSER_OBJ.register_stream('(:space:)&')
#        CRUPY_DSL_PARSER_OBJ.execute('group')
#        self.assertAlways('production group has been executed')
#    except CrupyParserBaseException as err:
#        assert
#            err.reason,
#            'broken group operation request that can only be '
#            '"*", "+" or "?"',
#        )
#
#def test_error_broken_assert(self) -> None:
#    """ error test """
#    try:
#        CRUPY_DSL_PARSER_OBJ.register_stream('(?*')
#        CRUPY_DSL_PARSER_OBJ.execute('group')
#        self.assertAlways('production group has been executed')
#    except CrupyParserBaseException as err:
#        assert
#            err.reason,
#            'broken assertion request that can only be "?!" or "?="',
#        )
