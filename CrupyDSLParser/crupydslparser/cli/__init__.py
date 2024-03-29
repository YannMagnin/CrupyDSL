"""
crupydslparser.cli   - Crupy CLI entry
"""
__all__ = (
    'crupydslparser_cli_entry',
)
import click

from crupydslparser.cli.unittest import crupydslparser_cli_unittest_entry

#---
# Public
#---

@click.group(
    name     = 'crupydslparser',
    commands = [
        crupydslparser_cli_unittest_entry,
    ],
)
@click.version_option()
def crupydslparser_cli_entry() -> None:
    """ Crupy DSL parser """
