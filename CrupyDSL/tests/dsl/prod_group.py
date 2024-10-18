"""
tests.dsl.group - test group productions
"""
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpProductionCall,
    CrupyDSLLexerOpSeq,
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpBuiltin,
    CrupyDSLLexerOpOr,
    CrupyDSLLexerOpRep0N,
    CrupyDSLLexerOpRep1N,
    CrupyDSLLexerOpOptional,
    CrupyDSLLexerAssertLookaheadNegative,
    CrupyDSLLexerAssertLookaheadPositive,
)
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
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpProductionCall)
    assert operation._production_name == 'test_oui'

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
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpSeq)
    assert len(operation._seq) == 2
    assert isinstance(operation._seq[0], CrupyDSLLexerOpProductionCall)
    assert isinstance(operation._seq[1], CrupyDSLLexerOpText)
    assert operation._seq[0]._production_name == 'test_oui'
    assert operation._seq[1]._text == 'non'

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
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerAssertLookaheadNegative)
    assert len(operation._seq) == 1
    assert isinstance(operation._seq[0], CrupyDSLLexerOpText)
    assert operation._seq[0]._text == 'oui'

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
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerAssertLookaheadPositive)
    assert len(operation._seq) == 1
    assert isinstance(operation._seq[0], CrupyDSLLexerOpProductionCall)
    assert operation._seq[0]._production_name == 'space_opt'

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
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpRep0N)
    assert len(operation._seq) == 2
    assert isinstance(operation._seq[0], CrupyDSLLexerOpProductionCall)
    assert isinstance(operation._seq[1], CrupyDSLLexerOpBuiltin)
    assert operation._seq[0]._production_name == 'space_opt'
    assert operation._seq[1]._operation == 'any'

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
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpRep1N)
    assert len(operation._seq) == 1
    assert isinstance(operation._seq[0], CrupyDSLLexerOpOr)
    assert len(operation._seq[0]._seq) == 2
    assert isinstance(operation._seq[0]._seq[0], CrupyDSLLexerOpBuiltin)
    assert isinstance(operation._seq[0]._seq[1], CrupyDSLLexerOpText)
    assert operation._seq[0]._seq[0]._operation == 'any'
    assert operation._seq[0]._seq[1]._text == '2617'

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
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpOptional)
    assert len(operation._seq) == 1
    assert isinstance(operation._seq[0], CrupyDSLLexerOpOr)
    assert len(operation._seq[0]._seq) == 2
    assert isinstance(operation._seq[0]._seq[0], CrupyDSLLexerOpBuiltin)
    assert isinstance(operation._seq[0]._seq[1], CrupyDSLLexerOpSeq)
    assert operation._seq[0]._seq[0]._operation == 'any'
    assert len(operation._seq[0]._seq[1]._seq) == 2
    assert isinstance(
        operation._seq[0]._seq[1]._seq[0],
        CrupyDSLLexerOpText,
    )
    assert isinstance(
        operation._seq[0]._seq[1]._seq[1],
        CrupyDSLLexerOpProductionCall,
    )
    assert operation._seq[0]._seq[1]._seq[0]._text == '2617'
    assert operation._seq[0]._seq[1]._seq[1]._production_name == 'rte'

## error

def test_error_start() -> None:
    """ error test """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('oui_non)')
        CRUPY_DSL_PARSER_OBJ.execute('group')
        raise AssertionError('production \'group\' executed')
    except CrupyDSLParserBaseException as err:
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
    except CrupyDSLParserBaseException as err:
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
# > Since we use the CrupyDSLLexerOpOptional() to fetch group operation,
#   we cannot catch the CrupyDSLLexerOpError() because it will be ignored
#   by the optional behaviour
#
#def test_error_broken_operation(self) -> None:
#    """ error test """
#    try:
#        CRUPY_DSL_PARSER_OBJ.register_stream('(:space:)&')
#        CRUPY_DSL_PARSER_OBJ.execute('group')
#        self.assertAlways('production group has been executed')
#    except CrupyDSLParserBaseException as err:
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
#    except CrupyDSLParserBaseException as err:
#        assert
#            err.reason,
#            'broken assertion request that can only be "?!" or "?="',
#        )
