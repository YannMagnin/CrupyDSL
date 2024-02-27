"""
example.crupyjson._grammar  - high-level JSON grammar definition
"""
from crupydslparser.core.grammar import CrupyGrammarBase

#---
# Internals
#---

class _CrupyGrammarJSON(CrupyGrammarBase):
    """ define JSON grammar using Crupy DSL
    """
    production_entry    = 'json'
    grammar             = """
        <json>      ::= <primitive> | <container>

        <primitive> ::= <number> | <string> | <boolean> | <nullable>
        <number>    ::= "[0-9]+"
        <string>    ::= "\".*\"" | "'.*'"
        <boolean>   ::= "true" | "false"
        <nullable>  ::= "null"

        <container> ::= <object> | <array>
        <array>     ::= "[" <json> ("," <json>)*  "]"
        <object>    ::= "{" <member> ("," <member>)*  "}"
        <member>    ::= <string> ":" <json>
    """
