"""
crupydsl.grammar._dsl._parser  - manual DSL parser
"""
__all__ = [
    'CrupyDSLParserException',
    'CRUPY_DSL_PARSER_OBJ',
]
from crupydsl.grammar._dsl._parser.exception import (
    CrupyDSLParserException,
)
from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpSeq,
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpProductionCall,
    CrupyDSLLexerOpRep0N,
    CrupyDSLLexerOpRep1N,
    CrupyDSLLexerOpOr,
    CrupyDSLLexerOpBuiltin,
    CrupyDSLLexerOpOptional,
    CrupyDSLLexerOpError,
    CrupyDSLLexerAssertLookaheadNegative,
    CrupyDSLLexerAssertLookaheadPositive,
)
from crupydsl.grammar._dsl._parser.prod_dsl import dsl_dsl_hook
from crupydsl.grammar._dsl._parser.prod_eol import dsl_eol_hook
from crupydsl.grammar._dsl._parser.prod_space import dsl_space_hook
from crupydsl.grammar._dsl._parser.prod_builtin import (
    dsl_builtin_hook,
    dsl_builtin_hook_error,
)
from crupydsl.grammar._dsl._parser.prod_statement import (
    dsl_statement_hook,
)
from crupydsl.grammar._dsl._parser.prod_group import (
    dsl_group_hook,
    dsl_group_hook_error,
)
from crupydsl.grammar._dsl._parser.prod_production import (
    dsl_production_hook,
    dsl_production_hook_error,
)
from crupydsl.grammar._dsl._parser.prod_string import (
    dsl_string_hook,
    dsl_string_hook_error,
)
from crupydsl.grammar._dsl._parser.prod_alternative import (
    dsl_alternative_hook,
)
from crupydsl.grammar._dsl._parser.prod_production_name import (
    dsl_production_name_hook,
    dsl_production_name_hook_error,
)
from crupydsl.grammar._dsl._parser.prod_error import (
    dsl_error_hook,
    dsl_error_hook_error,
)
from crupydsl.grammar._dsl._parser.prod_between import (
    dsl_between_hook,
    dsl_between_hook_error,
)

#---
# Public
#---

## productions description

CRUPY_DSL_PARSER_OBJ = CrupyDSLParserBase({
    #
    # Production entry
    # > <crupy_dsl> ::= (<crupy_dsl_production>)+ :eof:
    #
    'crupy_dsl' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpRep1N(
                CrupyDSLLexerOpProductionCall('production'),
            ),
            CrupyDSLLexerOpOptional(
                CrupyDSLLexerOpProductionCall('space_any'),
            ),
            CrupyDSLLexerOpBuiltin('eof'),
        ),
    #
    # Production (rule) declaration
    # > production ::= \
    #       <space_any> \
    #       <production_name> \
    #       <space> \
    #       "::=" \
    #       <space> \
    #       <statements> \
    #       <eol>
    # (error will be hooked)
    #
    'production' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpOptional(
                CrupyDSLLexerOpProductionCall('space_any'),
            ),
            CrupyDSLLexerOpProductionCall('production_name'),
            CrupyDSLLexerOpProductionCall('space'),
            CrupyDSLLexerOpText("::="),
            CrupyDSLLexerOpProductionCall('space'),
            CrupyDSLLexerOpProductionCall('statement'),
            CrupyDSLLexerOpProductionCall('eol'),
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
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpProductionCall('space_opt'),
            CrupyDSLLexerOpOptional(
                CrupyDSLLexerOpText('|'),
                CrupyDSLLexerOpProductionCall('space_opt'),
            ),
            CrupyDSLLexerOpProductionCall('alternative'),
            CrupyDSLLexerOpRep0N(
                CrupyDSLLexerOpProductionCall('space_opt'),
                CrupyDSLLexerOpText('|'),
                CrupyDSLLexerOpProductionCall('space_opt'),
                CrupyDSLLexerOpProductionCall('alternative'),
            ),
        ),
    #
    # Production' alternatives (right part of the production declaraction,
    # but without the "or" ("|") operation)
    # > alternative ::= (<production_name> | <group> | <string>)+
    #
    'alternative' : \
        CrupyDSLLexerOpRep1N(
            CrupyDSLLexerOpProductionCall('space_opt'),
            CrupyDSLLexerOpOr(
                CrupyDSLLexerOpProductionCall('between'),
                CrupyDSLLexerOpProductionCall('production_name'),
                CrupyDSLLexerOpProductionCall('string'),
                CrupyDSLLexerOpProductionCall('builtin'),
                CrupyDSLLexerOpProductionCall('group'),
                CrupyDSLLexerOpProductionCall('error')
            ),
        ),
    #
    # Group operation in production's alternatives
    # > group ::= "(" ("?" ("!"|"="))? <statement> ")" ("*"|"+"|"?")?
    # (error will be hooked)
    #
    'group' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpText('('),
            CrupyDSLLexerOpOptional(
                CrupyDSLLexerOpText("?"),
                CrupyDSLLexerOpOr(
                    CrupyDSLLexerOpText('!'),
                    CrupyDSLLexerOpText('='),
                    CrupyDSLLexerOpError(
                        'broken assertion request that can only be '
                        '"?!" or "?="',
                    ),
                ),
            ),
            CrupyDSLLexerOpProductionCall('space_opt'),
            CrupyDSLLexerOpProductionCall('statement'),
            CrupyDSLLexerOpProductionCall('space_opt'),
            CrupyDSLLexerOpText(')'),
            CrupyDSLLexerOpOptional(
                CrupyDSLLexerOpOr(
                    CrupyDSLLexerOpText('*'),
                    CrupyDSLLexerOpText('+'),
                    CrupyDSLLexerOpText('?'),
                    CrupyDSLLexerOpError(
                        'broken group operation request that can only be '
                        '"*", "+" or "?"',
                    ),
                ),
            ),
        ),
    #
    # between production
    # > between ::= \
    #       (<production_name>|<string>|<buitin>|<group>) \
    #       ("..."|".!.") \
    #       (<production_name>|<string>|<buitin>|<group>)
    #
    'between' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpOr(
                CrupyDSLLexerOpProductionCall('production_name'),
                CrupyDSLLexerOpProductionCall('string'),
                CrupyDSLLexerOpProductionCall('builtin'),
                CrupyDSLLexerOpProductionCall('group'),
            ),
            CrupyDSLLexerOpOr(
                CrupyDSLLexerOpText('...'),
                CrupyDSLLexerOpText('.!.'),
            ),
            CrupyDSLLexerOpOr(
                CrupyDSLLexerOpProductionCall('production_name'),
                CrupyDSLLexerOpProductionCall('string'),
                CrupyDSLLexerOpProductionCall('builtin'),
                CrupyDSLLexerOpProductionCall('group'),
            ),
        ),
    #
    # string production
    # > string ::= \
    #       | "\"" ((?!"\"") :any:)* "\"" \
    #       | "'" ((?!"'") :any:)* "'"
    # (error will be hooked)
    #
    'string' :  \
        CrupyDSLLexerOpOr(
            CrupyDSLLexerOpSeq(
                CrupyDSLLexerOpText('"'),
                CrupyDSLLexerOpRep0N(
                    CrupyDSLLexerAssertLookaheadNegative(
                        CrupyDSLLexerOpText('"'),
                    ),
                    CrupyDSLLexerOpBuiltin('any')
                ),
                CrupyDSLLexerOpText('"'),
            ),
            CrupyDSLLexerOpSeq(
                CrupyDSLLexerOpText('\''),
                CrupyDSLLexerOpRep0N(
                    CrupyDSLLexerAssertLookaheadNegative(
                        CrupyDSLLexerOpText('\''),
                    ),
                    CrupyDSLLexerOpBuiltin('any')
                ),
                CrupyDSLLexerOpText('\''),
            ),
        ),
    #
    # Production name
    # > production_name ::= "<" (:alpha_lower: | "_")+ ">"
    # (error will be hooked)
    #
    'production_name' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpText('<'),
            CrupyDSLLexerOpRep1N(
                CrupyDSLLexerOpOr(
                    CrupyDSLLexerOpBuiltin('alpha_lower'),
                    CrupyDSLLexerOpText('_')
                ),
            ),
            CrupyDSLLexerOpText('>'),
        ),
    #
    # Builtin name
    # > builtin ::= ":" (:alphanum_lower: | "_")+ ":"
    # (error will be hooked)
    #
    'builtin' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpText(':'),
            CrupyDSLLexerOpRep1N(
                CrupyDSLLexerOpOr(
                    CrupyDSLLexerOpBuiltin('alphanum_lower'),
                    CrupyDSLLexerOpText('_')
                )
            ),
            CrupyDSLLexerOpText(':'),
        ),
    #
    # manual error
    # > error ::= "@" ("error"|"error_hook") "(" <string> ")"
    # (error will be hooked)
    #
    'error' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpText('@'),
            CrupyDSLLexerOpOr(
                CrupyDSLLexerOpText('error_hook'),
                CrupyDSLLexerOpText('error'),
            ),
            CrupyDSLLexerOpText('('),
            CrupyDSLLexerOpProductionCall('string'),
            CrupyDSLLexerOpText(')')
        ),

    #
    # space_any
    # space_any ::= (:space: | "\n" | "\r\n")*
    #
    'space_any' : \
        CrupyDSLLexerOpRep0N(
            CrupyDSLLexerOpOr(
                CrupyDSLLexerOpBuiltin('space'),
                CrupyDSLLexerOpText('\n'),
                CrupyDSLLexerOpText('\r\n'),
            ),
        ),
    #
    # space_opt
    # space_opt ::= (<__space>)*
    #
    'space_opt' : \
        CrupyDSLLexerOpRep0N(
            CrupyDSLLexerOpProductionCall('__space'),
        ),
    #
    # space
    # > space ::= (<__space>)+
    #
    'space' : \
        CrupyDSLLexerOpOr(
            CrupyDSLLexerOpRep1N(
                CrupyDSLLexerOpProductionCall('__space'),
            ),
            CrupyDSLLexerOpError('missing at least one space'),
        ),
    #
    # __space
    # > __space ::= :space: | ((?="\") <eol>) | @error('not a space')
    #
    '__space' : \
        CrupyDSLLexerOpOr(
            CrupyDSLLexerOpBuiltin('space'),
            CrupyDSLLexerOpSeq(
                CrupyDSLLexerAssertLookaheadPositive(
                    CrupyDSLLexerOpText('\\'),
                    CrupyDSLLexerOpProductionCall('eol'),
                ),
                CrupyDSLLexerOpText('\\'),
                CrupyDSLLexerOpProductionCall('eol'),
            ),
            CrupyDSLLexerOpError('not a space'),
        ),
    #
    # end-of-line
    # > eol ::= :newline: | :eof: | @error('not an end-of-line')
    #
    'eol' : \
        CrupyDSLLexerOpOr(
            CrupyDSLLexerOpBuiltin('newline'),
            CrupyDSLLexerOpBuiltin('eof'),
            CrupyDSLLexerOpError('not an end-of-file'),
        ),
})

## hook registration

CRUPY_DSL_PARSER_OBJ.register_post_hook('eol', dsl_eol_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook('space', dsl_space_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook('space_any', dsl_space_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook('space_opt', dsl_space_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook('__space', dsl_space_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook('builtin', dsl_builtin_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook('string', dsl_string_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook('group', dsl_group_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook('error', dsl_error_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook('crupy_dsl', dsl_dsl_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook('statement', dsl_statement_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook('production', dsl_production_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook('between', dsl_between_hook)
CRUPY_DSL_PARSER_OBJ.register_post_hook(
    'alternative',
    dsl_alternative_hook,
)
CRUPY_DSL_PARSER_OBJ.register_post_hook(
    'production_name',
    dsl_production_name_hook,
)

## hook error registration

CRUPY_DSL_PARSER_OBJ.register_error_hook('string', dsl_string_hook_error)
CRUPY_DSL_PARSER_OBJ.register_error_hook('builtin', dsl_builtin_hook_error)
CRUPY_DSL_PARSER_OBJ.register_error_hook('between', dsl_between_hook_error)
CRUPY_DSL_PARSER_OBJ.register_error_hook('group', dsl_group_hook_error)
CRUPY_DSL_PARSER_OBJ.register_error_hook('error', dsl_error_hook_error)
CRUPY_DSL_PARSER_OBJ.register_error_hook(
    'production',
    dsl_production_hook_error,
)
CRUPY_DSL_PARSER_OBJ.register_error_hook(
    'production_name',
    dsl_production_name_hook_error,
)
