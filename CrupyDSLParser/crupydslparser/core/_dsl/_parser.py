"""
crupydslparser.core._dsl._rules  - define manually all grammar rule of DSL
"""
__all__ = [
    'CRUPY_DSL_PARSER_OBJ',
]

from crupydslparser.core.parser import CrupyParserBase
from crupydslparser.core._lexer import (
    CrupyLexerOpSeq,
    CrupyLexerOpText,
    CrupyLexerOpProductionCall,
    CrupyLexerOpRep0N,
    CrupyLexerOpRep1N,
    CrupyLexerOpOr,
    CrupyLexerOpBetween,
)
from crupydslparser.core._dsl._hook_dsl_production_name import (
    hook_dsl_production_name,
)

#---
# Public
#---

## productions description

CRUPY_DSL_PARSER_OBJ = CrupyParserBase({
    #
    # Production (rule) declaration
    # > crupy_dsl_production ::= \
    #       <crupy_dsl_rulename> "::=" <crupy_dsl_stmts>
    #
    'crupy_dsl_production' : \
        CrupyLexerOpSeq(
            CrupyLexerOpProductionCall('crupy_dsl_rulename'),
            CrupyLexerOpText("::="),
            CrupyLexerOpProductionCall('crupy_dsl_stmts'),
        ),

    #
    # Production' statement declaration (right part of the production
    # declaration)
    # > crupy_dsl_stmts ::= <crupy_dsl_alts> [ "|" <crupy_dsl_alts> ]*
    #
    'crupy_dsl_stmts' : \
        CrupyLexerOpSeq(
            CrupyLexerOpProductionCall('crupy_dsl_alts'),
            CrupyLexerOpRep0N(
                CrupyLexerOpText('|'),
                CrupyLexerOpProductionCall('crupy_dsl_alts'),
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
    'crupy_dsl_alts' : \
        CrupyLexerOpRep1N(
            CrupyLexerOpOr(
                CrupyLexerOpProductionCall('crupy_dsl_production_name'),
                CrupyLexerOpProductionCall('crupy_dsl_group'),
                CrupyLexerOpProductionCall('crupy_dsl_strop'),
            ),
        ),

    #
    # String operation (support regex)
    # > crupy_dsl_strop ::= "\"" --special regex abstract-- "\""
    #
    'crupy_dsl_strop' : CrupyLexerOpBetween('"'),

    #
    # Group operation in production's alternatives
    # > crupy_dsl_group ::= "(" <crupy_dsl_stmts> ")[+?-]"
    #
    'crupy_dsl_group' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText('('),
            CrupyLexerOpProductionCall('crupy_dsl_stmts'),
            CrupyLexerOpText(')'),
            CrupyLexerOpOr(
                CrupyLexerOpText('+'),
                CrupyLexerOpText('?'),
                CrupyLexerOpText('-'),
            ),
        ),

    #
    # Production name
    # > crupy_dsl_production_name ::= "<[a-z_]+>"
    #
    'crupy_dsl_production_name' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText('<'),
            CrupyLexerOpRep1N(
                CrupyLexerOpOr(
                    CrupyLexerOpProductionCall('crupy_dsl_alphabet_lower'),
                    CrupyLexerOpText('_')
                ),
            ),
            CrupyLexerOpText('>'),
        ),

    #
    # Basic alphabetic in lowercase
    # > crupy_dsl_alphabet_lower : 'a' .. 'z'
    #
    'crupy_dsl_alphabet_lower' : \
        CrupyLexerOpOr(
            CrupyLexerOpText('a'),
            CrupyLexerOpText('b'),
            CrupyLexerOpText('c'),
            CrupyLexerOpText('d'),
            CrupyLexerOpText('e'),
            CrupyLexerOpText('f'),
            CrupyLexerOpText('g'),
            CrupyLexerOpText('h'),
            CrupyLexerOpText('i'),
            CrupyLexerOpText('j'),
            CrupyLexerOpText('k'),
            CrupyLexerOpText('l'),
            CrupyLexerOpText('m'),
            CrupyLexerOpText('n'),
            CrupyLexerOpText('o'),
            CrupyLexerOpText('p'),
            CrupyLexerOpText('q'),
            CrupyLexerOpText('r'),
            CrupyLexerOpText('s'),
            CrupyLexerOpText('t'),
            CrupyLexerOpText('u'),
            CrupyLexerOpText('v'),
            CrupyLexerOpText('w'),
            CrupyLexerOpText('x'),
            CrupyLexerOpText('y'),
            CrupyLexerOpText('z'),
        ),
})
CRUPY_DSL_PARSER_OBJ.register_hook(
    'crupy_dsl_production_name',
    hook_dsl_production_name,
)
