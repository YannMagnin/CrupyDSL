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
    CrupyLexerOpBuiltin,
    CrupyLexerOpOptional,
    CrupyLexerAssertEOF,
    CrupyLexerAssertLookaheadNegative,
    CrupyLexerAssertLookaheadPositive,
)
from crupydslparser.core._dsl._parser.eol import dsl_eol_hook
from crupydslparser.core._dsl._parser.space import dsl_space_hook
from crupydslparser.core._dsl._parser.builtin import dsl_builtin_hook
from crupydslparser.core._dsl._parser.string import dsl_string_hook
from crupydslparser.core._dsl._parser.statement import dsl_statement_hook
from crupydslparser.core._dsl._parser.group import dsl_group_hook
from crupydslparser.core._dsl._parser.production import dsl_production_hook
from crupydslparser.core._dsl._parser.alternative import (
    dsl_alternative_hook,
)
from crupydslparser.core._dsl._parser.production_name import (
    dsl_production_name_hook,
)

#---
# Public
#---

## productions description

CRUPY_DSL_PARSER_OBJ = CrupyParserBase({
    #
    # Production entry
    # > <crupy_dsl> ::= (<crupy_dsl_production>)+ :eof:
    #
    'crupy_dsl' : \
        CrupyLexerOpSeq(
            CrupyLexerOpRep1N(
                CrupyLexerOpProductionCall('production'),
            ),
            CrupyLexerOpBuiltin('eof'),
        ),
    #
    # Production (rule) declaration
    # > production ::= \
    #       <space_opt> \
    #       <crupy_dsl_rulename> \
    #       <crupy_dsl_space> \
    #       "::=" \
    #       <crupy_dsl_space> \
    #       <crupy_dsl_stmts> \
    #       <eol>
    #
    'production' : \
        CrupyLexerOpSeq(
            CrupyLexerOpProductionCall('space_opt'),
            CrupyLexerOpProductionCall('production_name'),
            CrupyLexerOpProductionCall('space'),
            CrupyLexerOpText("::="),
            CrupyLexerOpProductionCall('space'),
            CrupyLexerOpProductionCall('statement'),
            CrupyLexerOpProductionCall('eol'),
        ),
    #
    # Production' statement declaration (right part of a production)
    # > statement ::= \
    #       (<space_opt> "|" <space_opt>)? \
    #       <alternative> \
    #       (<space_opt> "|" <space_opt> <alternative>)* \
    #       <eol>
    #
    'statement' : \
        CrupyLexerOpSeq(
            CrupyLexerOpProductionCall('space_opt'),
            CrupyLexerOpOptional(
                CrupyLexerOpText('|'),
                CrupyLexerOpProductionCall('space_opt'),
            ),
            CrupyLexerOpProductionCall('alternative'),
            CrupyLexerOpRep0N(
                CrupyLexerOpProductionCall('space_opt'),
                CrupyLexerOpText('|'),
                CrupyLexerOpProductionCall('space_opt'),
                CrupyLexerOpProductionCall('alternative'),
            ),
        ),
    #
    # Production' alternatives (right part of the production declaraction,
    # but without the "or" ("|") operation)
    # > alternative ::= (<production_name> | <group> | <string>)+
    #
    'alternative' : \
        CrupyLexerOpRep1N(
            CrupyLexerOpProductionCall('space_opt'),
            CrupyLexerOpOr(
                CrupyLexerOpProductionCall('production_name'),
                CrupyLexerOpProductionCall('group'),
                CrupyLexerOpProductionCall('string'),
                CrupyLexerOpProductionCall('builtin'),
            ),
        ),
    #
    # Group operation in production's alternatives
    # > group ::= "(" ("?" ("+"|"-"|"!"|"="))? <statement> ")"
    #
    'group' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText('('),
            CrupyLexerOpOptional(
                CrupyLexerOpText("?"),
                CrupyLexerOpOr(
                    CrupyLexerOpText('!'),
                    CrupyLexerOpText('='),
                ),
            ),
            CrupyLexerOpProductionCall('space_opt'),
            CrupyLexerOpProductionCall('statement'),
            CrupyLexerOpProductionCall('space_opt'),
            CrupyLexerOpText(')'),
            CrupyLexerOpOptional(
                CrupyLexerOpOr(
                    CrupyLexerOpText('*'),
                    CrupyLexerOpText('+'),
                    CrupyLexerOpText('?'),
                ),
            ),
        ),
    #
    # String operation (support regex)
    # > string ::= "\"" ((?!"\"") :any:)+ "\""
    #
    'string' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText('"'),
            CrupyLexerOpRep1N(
                CrupyLexerAssertLookaheadNegative(
                    CrupyLexerOpText('"'),
                ),
                CrupyLexerOpBuiltin('any')
            ),
            CrupyLexerOpText('"'),
        ),
    #
    # Production name
    # > production_name ::= "<" (:alpha_lower | "_")+ ">"
    #
    'production_name' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText('<'),
            CrupyLexerOpRep1N(
                CrupyLexerOpOr(
                    CrupyLexerOpBuiltin('alpha_lower'),
                    CrupyLexerOpText('_')
                ),
            ),
            CrupyLexerOpText('>'),
        ),
    #
    # Builtin name
    # > builtin ::= ":" (:alpha_lower:)+ ":"
    #
    'builtin' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText(':'),
            CrupyLexerOpRep1N(
                CrupyLexerOpBuiltin('alpha_lower'),
            ),
            CrupyLexerOpText(':'),
        ),
    #
    # space_opt
    # space_opt ::= (:space: | ((?="\") <eol>)*
    #
    'space_opt' : \
        CrupyLexerOpRep0N(
            CrupyLexerOpProductionCall('__space'),
        ),
    #
    # space
    # > space ::= ()+
    #
    'space' : \
        CrupyLexerOpRep1N(
            CrupyLexerOpProductionCall('__space'),
        ),
    #
    # __space
    # > __space ::= :space: | ((?="\") <eol>)
    #
    '__space' : \
        CrupyLexerOpOr(
            CrupyLexerOpBuiltin('space'),
            CrupyLexerOpSeq(
                CrupyLexerAssertLookaheadPositive(
                    CrupyLexerOpText('\\'),
                    CrupyLexerOpProductionCall('eol'),
                ),
                CrupyLexerOpText('\\'),
                CrupyLexerOpProductionCall('eol'),
            ),
        ),
    #
    # end-of-line
    # > eol ::= "\n" | "\r\n"
    #
    'eol' : \
        CrupyLexerOpOr(
            CrupyLexerOpText('\n'),
            CrupyLexerOpText('\r\n'),
            CrupyLexerOpBuiltin('eof'),
        ),
})

## hook registration

CRUPY_DSL_PARSER_OBJ.register_hook(
    'production_name',
    dsl_production_name_hook,
)
CRUPY_DSL_PARSER_OBJ.register_hook('eol', dsl_eol_hook)
CRUPY_DSL_PARSER_OBJ.register_hook('space', dsl_space_hook)
CRUPY_DSL_PARSER_OBJ.register_hook('space_opt', dsl_space_hook)
CRUPY_DSL_PARSER_OBJ.register_hook('__space', dsl_space_hook)
CRUPY_DSL_PARSER_OBJ.register_hook('builtin', dsl_builtin_hook)
CRUPY_DSL_PARSER_OBJ.register_hook('string', dsl_string_hook)
CRUPY_DSL_PARSER_OBJ.register_hook('alternative', dsl_alternative_hook)
CRUPY_DSL_PARSER_OBJ.register_hook('statement', dsl_statement_hook)
CRUPY_DSL_PARSER_OBJ.register_hook('group', dsl_group_hook)
CRUPY_DSL_PARSER_OBJ.register_hook('production', dsl_production_hook)
