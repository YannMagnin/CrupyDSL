"""
crupydslparser.core._dsl._rules  - define manually all grammar rule of DSL
"""
__all__ = [
    'CRUPY_DSL_PARSER_OBJ',
]

from crupydslparser.core.parser._base import CrupyParserBase
from crupydslparser.core._lexer import (
    CrupyLexerSeq,
    CrupyLexerText,
    CrupyLexerProduction,
    CrupyLexerRep0N,
    CrupyLexerRep1N,
    CrupyLexerOr,
    CrupyLexerBetween,
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
        CrupyLexerSeq(
            CrupyLexerProduction('crupy_dsl_rulename'),
            CrupyLexerText("::="),
            CrupyLexerProduction('crupy_dsl_stmts'),
        ),

    #
    # Production' statement declaration (right part of the production
    # declaration)
    # > crupy_dsl_stmts ::= <crupy_dsl_alts> [ "|" <crupy_dsl_alts> ]*
    #
    'crupy_dsl_stmts' : \
        CrupyLexerSeq(
            CrupyLexerProduction('crupy_dsl_alts'),
            CrupyLexerRep0N(
                CrupyLexerText('|'),
                CrupyLexerProduction('crupy_dsl_alts'),
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
        CrupyLexerRep1N(
            CrupyLexerOr(
                CrupyLexerProduction('crupy_dsl_production_name'),
                CrupyLexerProduction('crupy_dsl_group'),
                CrupyLexerProduction('crupy_dsl_strop'),
            ),
        ),

    #
    # String operation (support regex)
    # > crupy_dsl_strop ::= "\"" --special regex abstract-- "\""
    #
    'crupy_dsl_strop' : CrupyLexerBetween('"'),

    #
    # Group operation in production's alternatives
    # > crupy_dsl_group ::= "(" <crupy_dsl_stmts> ")[+?-]"
    #
    'crupy_dsl_group' : \
        CrupyLexerSeq(
            CrupyLexerText('('),
            CrupyLexerProduction('crupy_dsl_stmts'),
            CrupyLexerText(')'),
            CrupyLexerOr(
                CrupyLexerText('+'),
                CrupyLexerText('?'),
                CrupyLexerText('-'),
            ),
        ),

    #
    # Production name
    # > crupy_dsl_production_name ::= "<[a-z_]+>"
    #
    'crupy_dsl_production_name' : \
        CrupyLexerSeq(
            CrupyLexerText('<'),
            CrupyLexerRep1N(
                CrupyLexerOr(
                    CrupyLexerProduction('crupy_dsl_alphabet_lower'),
                    CrupyLexerText('_')
                ),
            ),
            CrupyLexerText('>'),
        ),

    #
    # Basic alphabetic in lowercase
    # > crupy_dsl_alphabet_lower : 'a' .. 'z'
    #
    'crupy_dsl_alphabet_lower' : \
        CrupyLexerOr(
            CrupyLexerText('a'),
            CrupyLexerText('b'),
            CrupyLexerText('c'),
            CrupyLexerText('d'),
            CrupyLexerText('e'),
            CrupyLexerText('f'),
            CrupyLexerText('g'),
            CrupyLexerText('h'),
            CrupyLexerText('i'),
            CrupyLexerText('j'),
            CrupyLexerText('k'),
            CrupyLexerText('l'),
            CrupyLexerText('m'),
            CrupyLexerText('n'),
            CrupyLexerText('o'),
            CrupyLexerText('p'),
            CrupyLexerText('q'),
            CrupyLexerText('r'),
            CrupyLexerText('s'),
            CrupyLexerText('t'),
            CrupyLexerText('u'),
            CrupyLexerText('v'),
            CrupyLexerText('w'),
            CrupyLexerText('x'),
            CrupyLexerText('y'),
            CrupyLexerText('z'),
        ),
})
CRUPY_DSL_PARSER_OBJ.register_hook(
    'crupy_dsl_production_name',
    hook_dsl_production_name,
)
