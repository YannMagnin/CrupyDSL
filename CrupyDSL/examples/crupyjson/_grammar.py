"""
example.crupyjson._grammar  - high-level JSON grammar definition
"""
__all__ = [
    'CrupyDSLGrammarJSON',
]

from crupydsl.parser import CrupyDSLParserNodeBase
from crupydsl.grammar import CrupyDSLGrammarBase

from crupyjson._parser import (
    json_parser_prod_hook_nullable,
    json_parser_prod_hook_boolean,
    json_parser_prod_hook_string,
    json_parser_prod_hook_json,
    json_parser_prod_hook_container,
    json_parser_prod_hook_primitive,
    json_parser_prod_hook_array,
    json_parser_prod_hook_object,
    json_parser_prod_hook_member,
    json_parser_prod_hook_statement,
)

#---
# Public
#---

class CrupyDSLGrammarJSON(CrupyDSLGrammarBase):
    """ define JSON grammar using Crupy DSL
    """
    production_entry    = 'json'
    grammar             = r"""
        <json>      ::= <statement> <sp> :eof:
        <statement> ::= <primitive> | <container>

        <primitive> ::= :number: | <string> | <boolean> | <nullable>

        <container> ::= <object> | <array>
        <array>     ::= <sp> '[' <sp> <statement> (<sp> ',' <sp> <statement>)* <sp> ']' <sp>
        <object>    ::= <sp> '{' <sp> <member> ( <sp> ',' <sp> <member>)* <sp> '}' <sp>
        <member>    ::= <string> <sp> ':' <sp> <statement>

        <sp>        ::= (:space_newline:)*
        <boolean>   ::= 'true' | 'false'
        <nullable>  ::= 'null'
        <string>    ::= '"'...'"' | "'"..."'"
    """

    #---
    # Production hook
    #---

    def _json(self, node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
        """ handle the `json` production """
        return json_parser_prod_hook_json(node)

    def _statement(self, node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
        """ handle the `statement` production """
        return json_parser_prod_hook_statement(node)

    def _primitive(self, node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
        """ handle the `primitive` production """
        return json_parser_prod_hook_primitive(node)

    def _string(self, node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
        """ handle the `string` production """
        return json_parser_prod_hook_string(node)

    def _boolean(self, node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
        """ handle the `boolean` production """
        return json_parser_prod_hook_boolean(node)

    def _nullable(self, node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
        """ handle the `nullable` production """
        return json_parser_prod_hook_nullable(node)

    def _container(self, node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
        """ handle the `contenainer` production """
        return json_parser_prod_hook_container(node)

    def _array(self, node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
        """ handle the `array` production """
        return json_parser_prod_hook_array(node)

    def _object(self, node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
        """ handle the `object` production """
        return json_parser_prod_hook_object(node)

    def _member(self, node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
        """ handle the `member` production """
        return json_parser_prod_hook_member(node)
