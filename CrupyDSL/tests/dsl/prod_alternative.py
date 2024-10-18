"""
tests.dsl.alternative - test alternative productions
"""
from crupydsl.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydsl.grammar._dsl import dsl_compil_grammar_node
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpBetween,
    CrupyDSLLexerOpBuiltin,
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpProductionCall,
    CrupyDSLLexerOpSeq,
    CrupyDSLLexerAssertLookaheadNegative,
)

# allow access private members to ensure that the DSL node translation has
# been correctly done
# pylint: disable=locally-disabled,W0212

#---
# Public
#---

## functional

def test_prodname() -> None:
    """ test
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('<test_oui>')
    node = CRUPY_DSL_PARSER_OBJ.execute('alternative')
    assert node.type == 'dsl_alternative'
    assert len(node.seq) == 1
    assert node.seq[0].type == 'dsl_production_name'
    assert node.seq[0].production_name == 'test_oui'
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpProductionCall)
    assert operation._production_name == 'test_oui'

def test_string() -> None:
    """ test
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('"667ekip"')
    node = CRUPY_DSL_PARSER_OBJ.execute('alternative')
    assert node.type == 'dsl_alternative'
    assert len(node.seq) == 1
    assert node.seq[0].type == 'dsl_string'
    assert node.seq[0].text == '667ekip'
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpText)
    assert operation._text == '667ekip'

def test_between() -> None:
    """ test
    """
    CRUPY_DSL_PARSER_OBJ.register_stream(':any:..."i"')
    node = CRUPY_DSL_PARSER_OBJ.execute('alternative')
    assert node.type == 'dsl_alternative'
    assert len(node.seq) == 1
    assert node.seq[0].type == 'dsl_between'
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpBetween)
    assert isinstance(operation._startop, CrupyDSLLexerOpBuiltin)
    assert isinstance(operation._endop, CrupyDSLLexerOpText)
    assert operation._startop._operation == 'any'
    assert operation._endop._text == 'i'

def test_builtin() -> None:
    """ test
    """
    CRUPY_DSL_PARSER_OBJ.register_stream(':any:')
    node = CRUPY_DSL_PARSER_OBJ.execute('alternative')
    assert node.type == 'dsl_alternative'
    assert len(node.seq) == 1
    assert node.seq[0].type == 'dsl_builtin'
    assert node.seq[0].kind == 'any'
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpBuiltin)
    assert operation._operation == 'any'

def test_simple_success() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream(
        '<test_oui> "test" :number: (?!"oui?")?'
    )
    node = CRUPY_DSL_PARSER_OBJ.execute('alternative')
    assert node.type == 'dsl_alternative'
    assert len(node.seq) == 4
    assert node.seq[0].type == 'dsl_production_name'
    assert node.seq[0].production_name == 'test_oui'
    assert node.seq[1].type == 'dsl_string'
    assert node.seq[1].text == 'test'
    assert node.seq[2].type == 'dsl_builtin'
    assert node.seq[2].kind == 'number'
    assert node.seq[3].type == 'dsl_group'
    assert node.seq[3].lookahead == 'negative'
    assert node.seq[3].operation == 'optional'
    assert node.seq[3].statement.type == 'dsl_statement'
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpSeq)
    assert len(operation._seq) == 4
    assert isinstance(operation._seq[0], CrupyDSLLexerOpProductionCall)
    assert isinstance(operation._seq[1], CrupyDSLLexerOpText)
    assert isinstance(operation._seq[2], CrupyDSLLexerOpBuiltin)
    assert isinstance(
        operation._seq[3],
        CrupyDSLLexerAssertLookaheadNegative,
    )
    assert operation._seq[0]._production_name == 'test_oui'
    assert operation._seq[1]._text == 'test'
    assert operation._seq[2]._operation == 'number'
    assert len(operation._seq[3]._seq) == 1
    assert isinstance(operation._seq[3]._seq[0], CrupyDSLLexerOpText)
    assert operation._seq[3]._seq[0]._text == 'oui?'

## error

def test_error_broken_string() -> None:
    """ error test
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('"test oui')
    try:
        CRUPY_DSL_PARSER_OBJ.execute('alternative')
        raise AssertionError('production \'alternative\' executed')
    except CrupyDSLParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 10\n'
            '"test oui\n'
            '~~~~~~~~~^\n'
            'SyntaxError: missing enclosing quote'
        )
        assert err.reason == 'missing enclosing quote'

def test_error_broken_prodname() -> None:
    """ error test
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('<foo_barr')
    try:
        CRUPY_DSL_PARSER_OBJ.execute('alternative')
        raise AssertionError('production \'alternative\' executed')
    except CrupyDSLParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 10\n'
            '<foo_barr\n'
            '~~~~~~~~~^\n'
            'SyntaxError: missing enclosing chevron'
        )
        assert err.reason == 'missing enclosing chevron'

def test_error_broken_group() -> None:
    """ error test
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('("aaaaabb" ')
    try:
        CRUPY_DSL_PARSER_OBJ.execute('alternative')
        raise AssertionError('production \'alternative\' executed')
    except CrupyDSLParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 12\n'
            '("aaaaabb" \n'
            '~~~~~~~~~~~^\n'
            'SyntaxError: missing enclosing parenthesis'
        )
        assert err.reason == 'missing enclosing parenthesis'

def test_error_broken_any() -> None:
    """ error test
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream(':yo_man')
        CRUPY_DSL_PARSER_OBJ.execute('alternative')
        raise AssertionError('production \'alternative\' executed')
    except CrupyDSLParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 8\n'
            ':yo_man\n'
            '~~~~~~~^\n'
            'SyntaxError: missing enclosing colon'
        )
        assert err.reason == 'missing enclosing colon'
