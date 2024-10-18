"""
tests.dsl.dsl - test dsl productions
"""
from crupydsl.grammar._dsl import (
    CRUPY_DSL_PARSER_OBJ,
    dsl_compil_grammar_entry,
)
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpProductionCall,
    CrupyDSLLexerOpSeq,
)

# allow access private members to ensure that the DSL node translation has
# been correctly done
# pylint: disable=locally-disabled,W0212

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
    book = dsl_compil_grammar_entry(node)
    assert len(book) == 1
    assert 'entry' in book
    assert isinstance(book['entry'], CrupyDSLLexerOpSeq)
    assert len(book['entry']._seq) == 2
    assert isinstance(book['entry']._seq[0], CrupyDSLLexerOpText)
    assert isinstance(book['entry']._seq[1], CrupyDSLLexerOpProductionCall)
    assert book['entry']._seq[0]._text == 'yes'
    assert book['entry']._seq[1]._production_name == 'test'

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
    book = dsl_compil_grammar_entry(node)
    assert len(book) == 1
    assert 'entry' in book
    assert isinstance(book['entry'], CrupyDSLLexerOpSeq)
    assert len(book['entry']._seq) == 2
    assert isinstance(book['entry']._seq[0], CrupyDSLLexerOpText)
    assert isinstance(book['entry']._seq[1], CrupyDSLLexerOpProductionCall)
    assert book['entry']._seq[0]._text == 'yes'
    assert book['entry']._seq[1]._production_name == 'test'

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
    book = dsl_compil_grammar_entry(node)
    assert len(book) == 2
    assert 'entry' in book
    assert 'test' in book
    assert isinstance(book['entry'], CrupyDSLLexerOpSeq)
    assert len(book['entry']._seq) == 2
    assert isinstance(book['entry']._seq[0], CrupyDSLLexerOpText)
    assert isinstance(book['entry']._seq[1], CrupyDSLLexerOpProductionCall)
    assert book['entry']._seq[0]._text == 'yes'
    assert book['entry']._seq[1]._production_name == 'test'
    assert isinstance(book['test'], CrupyDSLLexerOpText)
    assert book['test']._text == 'test'

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
