"""
crupyjson._parser     - manual JSON parser object
"""
__all__ = [
    'JSON_PARSER_OBJ',
    'json_parser_prod_hook_nullable',
    'json_parser_prod_hook_boolean',
    'json_parser_prod_hook_string',
    'json_parser_prod_hook_json',
    'json_parser_prod_hook_container',
    'json_parser_prod_hook_primitive',
    'json_parser_prod_hook_array',
    'json_parser_prod_hook_object',
    'json_parser_prod_hook_member',
    'json_parser_prod_hook_statement',
]

from crupydsl.parser import CrupyDSLParserBase
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpSeq,
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpRep1N,
    CrupyDSLLexerOpRep0N,
    CrupyDSLLexerOpOr,
    CrupyDSLLexerOpProductionCall,
    CrupyDSLLexerOpBuiltin,
    CrupyDSLLexerOpBetween,
    CrupyDSLLexerAssertLookaheadNegative,
)

from crupyjson._parser.prod_nullable import json_parser_prod_hook_nullable
from crupyjson._parser.prod_boolean import json_parser_prod_hook_boolean
from crupyjson._parser.prod_string import json_parser_prod_hook_string
from crupyjson._parser.prod_json import json_parser_prod_hook_json
from crupyjson._parser.prod_container import json_parser_prod_hook_container
from crupyjson._parser.prod_primitive import json_parser_prod_hook_primitive
from crupyjson._parser.prod_array import json_parser_prod_hook_array
from crupyjson._parser.prod_object import json_parser_prod_hook_object
from crupyjson._parser.prod_member import json_parser_prod_hook_member
from crupyjson._parser.prod_statement import json_parser_prod_hook_statement

#---
# Public
#---

JSON_PARSER_OBJ = CrupyDSLParserBase({
    #
    # production entry
    # > json ::= (<primitive> | <container>) :eof:
    #
    'json' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpProductionCall('statement'),
            CrupyDSLLexerOpBuiltin('eof'),
        ),
    #
    # statement production
    # > statement ::= (<primitive> | <container>)
    #
    'statement' : \
        CrupyDSLLexerOpOr(
            CrupyDSLLexerOpProductionCall('primitive'),
            CrupyDSLLexerOpProductionCall('container'),
        ),
    #
    # primitive production
    # > primitive ::= :digit: | <string> | <boolean> | <nullable>
    #
    'primitive' : \
        CrupyDSLLexerOpOr(
            CrupyDSLLexerOpBuiltin('digit'),
            CrupyDSLLexerOpProductionCall('string'),
            CrupyDSLLexerOpProductionCall('boolean'),
            CrupyDSLLexerOpProductionCall('nullable'),
        ),
    #
    # container production
    # > container ::= <object> | <array>
    #
    'container' : \
        CrupyDSLLexerOpOr(
            CrupyDSLLexerOpProductionCall('object'),
            CrupyDSLLexerOpProductionCall('array'),
        ),
    #
    # array production
    # > array ::= "[" <statement> ("," <statement>)*  "]"
    #
    'array' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpText('['),
            CrupyDSLLexerOpProductionCall('statement'),
            CrupyDSLLexerOpRep0N(
                CrupyDSLLexerOpText(','),
                CrupyDSLLexerOpProductionCall('statement'),
            ),
            CrupyDSLLexerOpText(']'),
        ),
    #
    # object production
    # > object ::= "{" <member> ("," <member>)*  "}"
    #
    'object' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpText('{'),
            CrupyDSLLexerOpProductionCall('member'),
            CrupyDSLLexerOpRep0N(
                CrupyDSLLexerOpText(','),
                CrupyDSLLexerOpProductionCall('member'),
            ),
            CrupyDSLLexerOpText('}'),
        ),
    #
    # member production
    # > member ::= <string> ":" <statement>
    #
    'member' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpProductionCall('string'),
            CrupyDSLLexerOpText(':'),
            CrupyDSLLexerOpProductionCall('statement'),
        ),

    ## low-level

    #
    # string production
    # > string ::= \
    #       | "\"" ((?!"\"") :any:)* "\"" \
    #       | "'" ((?!"'") :any:)* "'"
    #
    'string' : \
        CrupyDSLLexerOpOr(
            CrupyDSLLexerOpBetween(
                startop         = CrupyDSLLexerOpText('"'),
                endop           = CrupyDSLLexerOpText('"'),
                with_newline    = False,
            ),
            CrupyDSLLexerOpBetween(
                startop         = CrupyDSLLexerOpText('\''),
                endop           = CrupyDSLLexerOpText('\''),
                with_newline    = False,
            ),
        ),
        #
        # boolean production
        # > boolean ::= "true" | "false"
        #
        'boolean' : \
            CrupyDSLLexerOpOr(
                CrupyDSLLexerOpText('true'),
                CrupyDSLLexerOpText('false'),
            ),
        #
        # nullable production
        # > nullable ::= "null"
        #
        'nullable' : \
            CrupyDSLLexerOpText('null'),
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
