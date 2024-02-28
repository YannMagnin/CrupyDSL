"""
crupyjson._parser     - manual JSON parser object
"""
__all__ = [
    'JSON_PARSER_OBJ',
]

from crupydslparser.core.parser import CrupyParserBase
from crupydslparser.core._lexer import (
    CrupyLexerOpSeq,
    CrupyLexerOpText,
    CrupyLexerOpRep1N,
    CrupyLexerOpRep0N,
    CrupyLexerOpOr,
    CrupyLexerOpProductionCall,
    CrupyLexerOpBuiltin,
    CrupyLexerAssertLookaheadNegative,
    CrupyLexerAssertEOF,
)

from crupyjson._parser.nullable import json_parser_prod_hook_nullable
from crupyjson._parser.boolean import json_parser_prod_hook_boolean
from crupyjson._parser.string import json_parser_prod_hook_string

#---
# Public
#---

JSON_PARSER_OBJ = CrupyParserBase({
    #
    # production entry
    # > json ::= (<primitive> | <container>) :eof:
    #
    'json' : \
        CrupyLexerOpSeq(
            CrupyLexerOpProductionCall('json_stmt'),
            CrupyLexerAssertEOF(),
        ),
    #
    # json_stmt production
    # > json_stmt ::= (<primitive> | <container>)
    #
    'json_stmt' : \
        CrupyLexerOpOr(
            CrupyLexerOpProductionCall('primitive'),
            CrupyLexerOpProductionCall('container'),
        ),
    #
    # primitive production
    # > primitive ::= :digit: | <string> | <boolean> | <nullable>
    #
    'primitive' : \
        CrupyLexerOpOr(
            CrupyLexerOpBuiltin('digit'),
            CrupyLexerOpProductionCall('string'),
            CrupyLexerOpProductionCall('boolean'),
            CrupyLexerOpProductionCall('nullable'),
        ),
    #
    # container production
    # > container ::= <object> | <array>
    #
    'container' : \
        CrupyLexerOpOr(
            CrupyLexerOpProductionCall('object'),
            CrupyLexerOpProductionCall('array'),
        ),
    #
    # array production
    # > array ::= "[" <json_stmt> ("," <json_stmt>)*  "]"
    #
    'array' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText('['),
            CrupyLexerOpProductionCall('json_stmt'),
            CrupyLexerOpRep0N(
                CrupyLexerOpText(','),
                CrupyLexerOpProductionCall('json_stmt'),
            ),
            CrupyLexerOpText(']'),
        ),
    #
    # object production
    # > object ::= "{" <member> ("," <member>)*  "}"
    #
    'object' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText('{'),
            CrupyLexerOpProductionCall('member'),
            CrupyLexerOpRep0N(
                CrupyLexerOpText(','),
                CrupyLexerOpProductionCall('member'),
            ),
            CrupyLexerOpText('}'),
        ),
    #
    # member production
    # > member ::= <string> ":" <json_stmt>
    #
    'member' : \
        CrupyLexerOpSeq(
            CrupyLexerOpProductionCall('string'),
            CrupyLexerOpText(':'),
            CrupyLexerOpProductionCall('json_stmt'),
        ),

    ## low-level

    #
    # string production
    # > string ::= \
    #       | "\"" ((?!"\"") :any:)* "\"" \
    #       | "'" ((?!"'") :any:)* "'"
    #
    'string' : \
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
        # boolean production
        # > boolean ::= "true" | "false"
        #
        'boolean' : \
            CrupyLexerOpOr(
                CrupyLexerOpText('true'),
                CrupyLexerOpText('false'),
            ),
        #
        # nullable production
        # > nullable ::= "null"
        #
        'nullable' : \
            CrupyLexerOpText('null'),
})

## register all hooks

JSON_PARSER_OBJ.register_hook('nullable', json_parser_prod_hook_nullable)
JSON_PARSER_OBJ.register_hook('boolean', json_parser_prod_hook_boolean)
JSON_PARSER_OBJ.register_hook('string', json_parser_prod_hook_string)
