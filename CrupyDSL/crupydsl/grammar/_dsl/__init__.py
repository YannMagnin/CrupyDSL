"""
crupydsl.grammar._dsl - DSL abstraction
"""
__all__ = [
    'CRUPY_DSL_PARSER_OBJ',
    'dsl_compil_grammar_statement',
]
from crupydsl.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydsl.grammar._dsl.compile import (
    dsl_compil_grammar_statement,
)
