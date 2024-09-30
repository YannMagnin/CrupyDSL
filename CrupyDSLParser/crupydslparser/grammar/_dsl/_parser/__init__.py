"""
crupydslparser.grammar._dsl._parser  - manual DSL parser
"""
__all__ = [
    'CrupyDslParserException',
    'CRUPY_DSL_PARSER_OBJ',
]
from crupydslparser.grammar._dsl._parser.exception import (
    CrupyDslParserException,
)
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpSeq,
    CrupyLexerOpText,
    CrupyLexerOpProductionCall,
    CrupyLexerOpRep0N,
    CrupyLexerOpRep1N,
    CrupyLexerOpOr,
    CrupyLexerOpBuiltin,
    CrupyLexerOpOptional,
    CrupyLexerOpError,
    CrupyLexerAssertLookaheadNegative,
    CrupyLexerAssertLookaheadPositive,
)
from crupydslparser.grammar._dsl._parser._dsl import dsl_dsl_hook
from crupydslparser.grammar._dsl._parser._eol import dsl_eol_hook
from crupydslparser.grammar._dsl._parser._space import dsl_space_hook
from crupydslparser.grammar._dsl._parser._builtin import (
    dsl_builtin_hook,
    dsl_builtin_hook_error,
)
from crupydslparser.grammar._dsl._parser._statement import (
    dsl_statement_hook,
)
from crupydslparser.grammar._dsl._parser._group import (
    dsl_group_hook,
    dsl_group_hook_error,
)
from crupydslparser.grammar._dsl._parser._production import (
    dsl_production_hook,
    dsl_production_hook_error,
)
from crupydslparser.grammar._dsl._parser._string import (
    dsl_string_hook,
    dsl_string_hook_error,
)
from crupydslparser.grammar._dsl._parser._alternative import (
    dsl_alternative_hook,
)
from crupydslparser.grammar._dsl._parser._production_name import (
    dsl_production_name_hook,
    dsl_production_name_hook_error,
)
from crupydslparser.grammar._dsl._parser._error import (
    dsl_error_hook,
    dsl_error_hook_error,
)
from crupydslparser.grammar._dsl._parser._between import (
    dsl_between_hook,
    dsl_between_hook_error,
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
            CrupyLexerOpOptional(
                CrupyLexerOpProductionCall('space_any'),
            ),
            CrupyLexerOpBuiltin('eof'),
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
        CrupyLexerOpSeq(
            CrupyLexerOpOptional(
                CrupyLexerOpProductionCall('space_any'),
            ),
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
                CrupyLexerOpProductionCall('between'),
                CrupyLexerOpProductionCall('production_name'),
                CrupyLexerOpProductionCall('string'),
                CrupyLexerOpProductionCall('builtin'),
                CrupyLexerOpProductionCall('group'),
                CrupyLexerOpProductionCall('error')
            ),
        ),
    #
    # Group operation in production's alternatives
    # > group ::= "(" ("?" ("!"|"="))? <statement> ")" ("*"|"+"|"?")?
    # (error will be hooked)
    #
    'group' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText('('),
            CrupyLexerOpOptional(
                CrupyLexerOpText("?"),
                CrupyLexerOpOr(
                    CrupyLexerOpText('!'),
                    CrupyLexerOpText('='),
                    CrupyLexerOpError(
                        'broken assertion request that can only be '
                        '"?!" or "?="',
                    ),
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
                    CrupyLexerOpError(
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
        CrupyLexerOpSeq(
            CrupyLexerOpOr(
                CrupyLexerOpProductionCall('production_name'),
                CrupyLexerOpProductionCall('string'),
                CrupyLexerOpProductionCall('builtin'),
                CrupyLexerOpProductionCall('group'),
            ),
            CrupyLexerOpOr(
                CrupyLexerOpText('...'),
                CrupyLexerOpText('.!.'),
            ),
            CrupyLexerOpOr(
                CrupyLexerOpProductionCall('production_name'),
                CrupyLexerOpProductionCall('string'),
                CrupyLexerOpProductionCall('builtin'),
                CrupyLexerOpProductionCall('group'),
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
        CrupyLexerOpOr(
            CrupyLexerOpSeq(
                CrupyLexerOpText('"'),
                CrupyLexerOpRep0N(
                    CrupyLexerAssertLookaheadNegative(
                        CrupyLexerOpText('"'),
                    ),
                    CrupyLexerOpBuiltin('any')
                ),
                CrupyLexerOpText('"'),
            ),
            CrupyLexerOpSeq(
                CrupyLexerOpText('\''),
                CrupyLexerOpRep0N(
                    CrupyLexerAssertLookaheadNegative(
                        CrupyLexerOpText('\''),
                    ),
                    CrupyLexerOpBuiltin('any')
                ),
                CrupyLexerOpText('\''),
            ),
        ),
    #
    # Production name
    # > production_name ::= "<" (:alpha_lower: | "_")+ ">"
    # (error will be hooked)
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
    # > builtin ::= ":" (:alphanum_lower: | "_")+ ":"
    # (error will be hooked)
    #
    'builtin' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText(':'),
            CrupyLexerOpRep1N(
                CrupyLexerOpOr(
                    CrupyLexerOpBuiltin('alphanum_lower'),
                    CrupyLexerOpText('_')
                )
            ),
            CrupyLexerOpText(':'),
        ),
    #
    # manual error
    # > error ::= "@" ("error"|"error_hook") "(" <string> ")"
    # (error will be hooked)
    #
    'error' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText('@'),
            CrupyLexerOpOr(
                CrupyLexerOpText('error_hook'),
                CrupyLexerOpText('error'),
            ),
            CrupyLexerOpText('('),
            CrupyLexerOpProductionCall('string'),
            CrupyLexerOpText(')')
        ),

    #
    # space_any
    # space_any ::= (:space: | "\n" | "\r\n")*
    #
    'space_any' : \
        CrupyLexerOpRep0N(
            CrupyLexerOpOr(
                CrupyLexerOpBuiltin('space'),
                CrupyLexerOpText('\n'),
                CrupyLexerOpText('\r\n'),
            ),
        ),
    #
    # space_opt
    # space_opt ::= (<__space>)*
    #
    'space_opt' : \
        CrupyLexerOpRep0N(
            CrupyLexerOpProductionCall('__space'),
        ),
    #
    # space
    # > space ::= (<__space>)+
    #
    'space' : \
        CrupyLexerOpOr(
            CrupyLexerOpRep1N(
                CrupyLexerOpProductionCall('__space'),
            ),
            CrupyLexerOpError('missing at least one space'),
        ),
    #
    # __space
    # > __space ::= :space: | ((?="\") <eol>) | @error('not a space')
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
            CrupyLexerOpError('not a space'),
        ),
    #
    # end-of-line
    # > eol ::= :newline: | :eof: | @error('not an end-of-line')
    #
    'eol' : \
        CrupyLexerOpOr(
            CrupyLexerOpBuiltin('newline'),
            CrupyLexerOpBuiltin('eof'),
            CrupyLexerOpError('not an end-of-file'),
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
