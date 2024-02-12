"""
crupydslparser.core._dsl._rules  - define manually all grammar rule of DSL
"""
__all__ = [
    'CRUPY_DSL_RULES',
]
from typing import Dict

from crupydslparser.core._lexer import (
    CrupyLexer,
    CrupyLexerSeq,
    CrupyLexerText,
    CrupyLexerMatcher,
    CrupyLexerRule,
    CrupyLexerRep0N,
    CrupyLexerRep1N,
    CrupyLexerOr,
    CrupyLexerUntil,
)

#---
# Public
#---

CRUPY_DSL_RULES: Dict[str,CrupyLexer] = {
    #
    # Production (rule) declaration
    # > crupy_dsl_production ::= \
    #       <crupy_dsl_rulename> "::=" <crupy_dsl_stmts>
    #
    'crupy_dsl_production' : CrupyLexerSeq(
        CrupyLexerRule('crupy_dsl_rulename'),
        CrupyLexerText("::="),
        CrupyLexerRule('crupy_dsl_stmts'),
    ),

    #
    # Production' statement declaration (right part of the production
    # declaration)
    # > crupy_dsl_stmts ::= <crupy_dsl_alts> [ "|" <crupy_dsl_alts> ]*
    #
    'crupy_dsl_stmts' : CrupyLexerSeq(
        CrupyLexerRule('crupy_dsl_alts'),
        CrupyLexerRep0N(
            CrupyLexerText('|'),
            CrupyLexerRule('crupy_dsl_alts'),
        ),
    ),

    #
    # Production' alternatives (right part of the production declaraction,
    # but without the "or" ("|") operation)
    # > crupy_dsl_alts ::= (
    #         <crupy_dsl_rulename>
    #       | <crupy_dsl_group>
    #       | <crupy_dsl_strop>
    #   )+
    #
    'crupy_dsl_alts' : CrupyLexerRep1N(
        CrupyLexerOr(
            CrupyLexerRule('crupy_dsl_production_name'),
            CrupyLexerRule('crupy_dsl_group'),
            CrupyLexerRule('crupy_dsl_strop'),
        ),
    ),

    #
    # String operation (support regex)
    # > crupy_dsl_strop ::= "\"" --special regex abstract-- "\""
    #
    'crupy_dsl_strop' : CrupyLexerUntil('"'),

    #
    # Group operation in production's alternatives
    # > crupy_dsl_group ::= "(" <crupy_dsl_stmts> ")[+?-]"
    #
    'crupy_dsl_group' : CrupyLexerSeq(
        CrupyLexerText('('),
        CrupyLexerRule('crupy_dsl_stmts'),
        CrupyLexerMatcher(')[+?-]'),
    ),

    #
    # Production name
    # > crupy_dsl_production_name ::= "<[a-z_]+>"
    #
    'crupy_dsl_production_name' : CrupyLexerMatcher("<[a-z_]+>"),
}
