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
        <json>      ::= <statement> :eof:
        <statement> ::= <primitive> | <container>

        <primitive> ::= :digit: | <string> | <boolean> | <nullable>
        <string>    ::= \
            | "\"" ((?!"\"") :any:)* "\"" \
            | "\'" ((?!"\'") :any:)* "\'"
        <boolean>   ::= "true" | "false"
        <nullable>  ::= "null"

        <container> ::= <object> | <array>
        <array>     ::= "[" <statement> ("," <statement>)*  "]"
        <object>    ::= "{" <member> ("," <member>)*  "}"
        <member>    ::= <string> ":" <statement>
    """
