"""
crupyjson.cli   - CLI entry
"""
__all__ = [
    'crupyjson_cli_entry',
]
import click

from crupyjson.cli.tests import crupyjson_cli_tests_entry
from crupyjson.cli.grammar import crupyjson_cli_grammar_entry

#---
# Public
#---

@click.group(
    'crupyjson',
    commands    = [
        crupyjson_cli_tests_entry,
        crupyjson_cli_grammar_entry
    ],
)
def crupyjson_cli_entry() -> None:
    """ JSON parser using crupy DSL """
