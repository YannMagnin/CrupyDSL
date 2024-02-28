"""
crupyjson.cli   - CLI entry
"""
__all__ = [
    'crupyjson_cli_entry',
]
import click

from crupyjson.cli.tests import crupyjson_cli_tests_entry

#---
# Public
#---

@click.group(
    'crupyjson',
    commands    = [
        crupyjson_cli_tests_entry,
    ],
)
def crupyjson_cli_entry() -> None:
    """ JSON parser using crupy DSL """
