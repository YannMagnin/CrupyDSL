"""
tests.dsl.string_fix - test string productions
"""
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.parser._lexer import CrupyDSLLexerOpText
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

def test_dquote_simple() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream(r'"667 oui ~# \\ dslk"')
    node = CRUPY_DSL_PARSER_OBJ.execute('string')
    assert node.type == 'dsl_string'
    assert node.text == r'667 oui ~# \ dslk'
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpText)
    assert operation._text == r'667 oui ~# \ dslk'

def test_dquote_escape() -> None:
    """ test escaping
    """
    CRUPY_DSL_PARSER_OBJ.register_stream('"\\"\\\\"')
    node = CRUPY_DSL_PARSER_OBJ.execute('string')
    assert node.type == 'dsl_string'
    assert node.text == '"\\'
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpText)
    assert operation._text == node.text

def test_quote_simple() -> None:
    """ simple valid case
    """
    CRUPY_DSL_PARSER_OBJ.register_stream(r"'667 oui ~# \\ dslk'")
    node = CRUPY_DSL_PARSER_OBJ.execute('string')
    assert node.type == 'dsl_string'
    assert node.text == r'667 oui ~# \ dslk'
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpText)
    assert operation._text == node.text

def test_quote_escape() -> None:
    """ test escaping
    """
    CRUPY_DSL_PARSER_OBJ.register_stream("'\\'\\\\'")
    node = CRUPY_DSL_PARSER_OBJ.execute('string')
    assert node.type == 'dsl_string'
    assert node.text == "'\\"
    operation = dsl_compil_grammar_node(node)
    assert isinstance(operation, CrupyDSLLexerOpText)
    assert operation._text == node.text

def test_error_enclose() -> None:
    """ test error handling
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('"allo?')
        CRUPY_DSL_PARSER_OBJ.execute('string')
        raise AssertionError('production \'string\' executed')
    except CrupyDSLParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 7\n'
            '"allo?\n'
            '~~~~~~^\n'
            'SyntaxError: missing enclosing quote'
        )

def test_error_open() -> None:
    """ test error handling
    """
    try:
        CRUPY_DSL_PARSER_OBJ.register_stream('allo?"')
        CRUPY_DSL_PARSER_OBJ.execute('string')
        raise AssertionError('production \'string\' executed')
    except CrupyDSLParserBaseException as err:
        assert str(err) == (
            'DSL parsing exception occured:\n'
            '\n'
            'Stream: line 1, column 1\n'
            'allo?"\n'
            '^\n'
            'SyntaxError: missing starting quote'
        )
