"""
tests.dsl.between - test between production
"""
from crupydsl.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.grammar._dsl import dsl_compil_grammar_node
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpBetween,
    CrupyDSLLexerOpBuiltin,
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpOr,
    CrupyDSLLexerOpRep1N,
    CrupyDSLLexerOpProductionCall,
    CrupyDSLLexerAssertLookaheadPositive,
)

# allow access private members to ensure that the DSL node translation has
# been correctly done
# pylint: disable=locally-disabled,W0212

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
    operation = dsl_compil_grammar_node(node0)
    assert isinstance(operation, CrupyDSLLexerOpBetween)
    assert isinstance(operation._startop, CrupyDSLLexerOpBuiltin)
    assert isinstance(operation._endop, CrupyDSLLexerOpText)
    assert operation._with_newline is False
    assert operation._startop._operation == 'digit'
    assert operation._endop._text == '\''

def test_simple_success_1() -> None:
    """ valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('<test_oui>.!.("aa"|:newline:)')
    node0 = CRUPY_DSL_PARSER_OBJ.execute('between')
    assert node0.type == 'dsl_between'
    assert node0.kind == 'newline'
    assert node0.opening.type == 'dsl_production_name'
    assert node0.closing.type == 'dsl_group'
    operation = dsl_compil_grammar_node(node0)
    assert isinstance(operation, CrupyDSLLexerOpBetween)
    assert isinstance(operation._startop, CrupyDSLLexerOpProductionCall)
    assert isinstance(operation._endop, CrupyDSLLexerOpOr)
    assert operation._with_newline is True
    assert operation._startop._production_name == 'test_oui'
    assert len(operation._endop._seq) == 2
    assert isinstance(operation._endop._seq[0], CrupyDSLLexerOpText)
    assert isinstance(operation._endop._seq[1], CrupyDSLLexerOpBuiltin)
    assert operation._endop._seq[0]._text == 'aa'
    assert operation._endop._seq[1]._operation == 'newline'

def test_simple_success_2() -> None:
    """ valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream(
        '("akc" :any:)+.!.(?=("aa"|:newline:))'
    )
    node0 = CRUPY_DSL_PARSER_OBJ.execute('between')
    assert node0.type == 'dsl_between'
    assert node0.kind == 'newline'
    assert node0.opening.type == 'dsl_group'
    assert node0.closing.type == 'dsl_group'
    operation = dsl_compil_grammar_node(node0)
    assert isinstance(operation, CrupyDSLLexerOpBetween)
    assert isinstance(operation._startop, CrupyDSLLexerOpRep1N)
    assert isinstance(operation._endop, CrupyDSLLexerAssertLookaheadPositive)
    assert operation._with_newline is True
    assert len(operation._startop._seq) == 2
    assert isinstance(operation._startop._seq[0], CrupyDSLLexerOpText)
    assert isinstance(operation._startop._seq[1], CrupyDSLLexerOpBuiltin)
    assert operation._startop._seq[0]._text == 'akc'
    assert operation._startop._seq[1]._operation == 'any'
    assert len(operation._endop._seq) == 1
    assert isinstance(operation._endop._seq[0], CrupyDSLLexerOpOr)
    assert len(operation._endop._seq[0]._seq) == 2
    assert isinstance(
        operation._endop._seq[0]._seq[0],
        CrupyDSLLexerOpText,
    )
    assert isinstance(
        operation._endop._seq[0]._seq[1],
        CrupyDSLLexerOpBuiltin,
    )
    assert operation._endop._seq[0]._seq[0]._text == 'aa'
    assert operation._endop._seq[0]._seq[1]._operation == 'newline'

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
