"""
example.json_grammar    - JSON grammar declaraction
"""
from typing import NoReturn
from pathlib import Path
import sys

import click

from crupy.core.grammar import CrupyGrammarBase

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

#---
# Public
#---

@click.command('json-parser')
@click.option(
    '-f', '--file', 'json_file_path',
    required    = True,
    help        = 'JSON file (valid or invalid)',
    type        = click.Path(
        exists          = True,
        file_okay       = True,
        dir_okay        = False,
        resolve_path    = True,
        path_type       = Path,
    ),
)
def jsonparser_cli_entry(json_file_path: Path) -> NoReturn:
    """ parse a simple JSON grammar """
    grammar = _CrupyGrammarJSON()
    grammar.parse(json_file_path)
    print(grammar)
    sys.exit(0)
