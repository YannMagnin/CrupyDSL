"""
crupy.core.grammar._dsl._rules  - define manually all grammar rule of DSL
"""
__all__ = [
    'CRUPY_DSL_RULES',
]
from typing import Dict, Any

from crupy.core.grammar._dsl._parser import (
    CrupyDslParserSeq,
    CrupyDslParserMatcher,
    CrupyDslParserString,
    CrupyDslParserRule,
    CrupyDslParserRep0N,
    CrupyDslParserRep1N,
    CrupyDslParserOr,
    CrupyDslParserUntil,
)

#---
# Public
#---

CRUPY_DSL_RULES: Dict[str,Any] = {
    #
    # Production (rule) declaration
    # > crupy_dsl_production ::= \
    #       <crupy_dsl_rulename> "::=" <crupy_dsl_stmts>
    #
    'crupy_dsl_production' : CrupyDslParserSeq(
        CrupyDslParserRule('crupy_dsl_rulename'),
        CrupyDslParserString("::="),
        CrupyDslParserRule('crupy_dsl_stmts'),
    ),

    #
    # Production' statement declaration (right part of the production
    # declaration)
    # > crupy_dsl_stmts ::= <crupy_dsl_alts> [ "|" <crupy_dsl_alts> ]*
    #
    'crupy_dsl_stmts' : CrupyDslParserSeq(
        CrupyDslParserRule('crupy_dsl_alts'),
        CrupyDslParserRep0N(
            CrupyDslParserString('|'),
            CrupyDslParserRule('crupy_dsl_alts'),
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
    'crupy_dsl_alts' : CrupyDslParserRep1N(
        CrupyDslParserOr(
            CrupyDslParserRule('crupy_dsl_production_name'),
            CrupyDslParserRule('crupy_dsl_group'),
            CrupyDslParserRule('crupy_dsl_strop'),
        ),
    ),

    #
    # String operation (support regex)
    # > crupy_dsl_strop ::= "\"" --special regex abstract-- "\""
    #
    'crupy_dsl_strop' : CrupyDslParserSeq(
        CrupyDslParserString('"'),
        CrupyDslParserUntil('"'),
    ),

    #
    # Group operation in production's alternatives
    # > crupy_dsl_group ::= "(" <crupy_dsl_stmts> ")[+?-]"
    #
    'crupy_dsl_group' : CrupyDslParserSeq(
        CrupyDslParserString('('),
        CrupyDslParserRule('crupy_dsl_stmts'),
        CrupyDslParserMatcher(')[+?-]'),
    ),

    #
    # Production name
    # > crupy_dsl_production_name ::= "<[a-z_]+>"
    #
    'crupy_dsl_production_name' : CrupyDslParserMatcher("<[a-z_]+>"),
}
