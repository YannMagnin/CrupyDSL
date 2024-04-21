"""
crupyjson._parser     - manual JSON parser object
"""
__all__ = [
    'JSON_PARSER_OBJ',
]

from crupydslparser.parser import CrupyParserBase
from crupydslparser.parser._lexer import (
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
from crupyjson._parser.json import json_parser_prod_hook_json
from crupyjson._parser.container import json_parser_prod_hook_container
from crupyjson._parser.primitive import json_parser_prod_hook_primitive
from crupyjson._parser.array import json_parser_prod_hook_array
from crupyjson._parser.object import json_parser_prod_hook_object
from crupyjson._parser.member import json_parser_prod_hook_member
from crupyjson._parser.statement import json_parser_prod_hook_statement

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
            CrupyLexerOpProductionCall('statement'),
            CrupyLexerAssertEOF(),
        ),
    #
    # statement production
    # > statement ::= (<primitive> | <container>)
    #
    'statement' : \
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
    # > array ::= "[" <statement> ("," <statement>)*  "]"
    #
    'array' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText('['),
            CrupyLexerOpProductionCall('statement'),
            CrupyLexerOpRep0N(
                CrupyLexerOpText(','),
                CrupyLexerOpProductionCall('statement'),
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
    # > member ::= <string> ":" <statement>
    #
    'member' : \
        CrupyLexerOpSeq(
            CrupyLexerOpProductionCall('string'),
            CrupyLexerOpText(':'),
            CrupyLexerOpProductionCall('statement'),
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

JSON_PARSER_OBJ.register_post_hook('array', json_parser_prod_hook_array)
JSON_PARSER_OBJ.register_post_hook('object', json_parser_prod_hook_object)
JSON_PARSER_OBJ.register_post_hook('member', json_parser_prod_hook_member)
JSON_PARSER_OBJ.register_post_hook('boolean', json_parser_prod_hook_boolean)
JSON_PARSER_OBJ.register_post_hook('string', json_parser_prod_hook_string)
JSON_PARSER_OBJ.register_post_hook('json', json_parser_prod_hook_json)
JSON_PARSER_OBJ.register_post_hook(
    'nullable',
    json_parser_prod_hook_nullable,
)
JSON_PARSER_OBJ.register_post_hook(
    'container',
    json_parser_prod_hook_container,
)
JSON_PARSER_OBJ.register_post_hook(
    'primitive',
    json_parser_prod_hook_primitive,
)
JSON_PARSER_OBJ.register_post_hook(
    'statement',
    json_parser_prod_hook_statement,
)
