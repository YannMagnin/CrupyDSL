"""
crupydsltester.cli   - Crupy CLI entry
"""
__all__ = [
    'crupydsltester_cli_entry',
]
import click

from crupydsltester.cli.unittest import crupydsltester_cli_unittest_entry

#---
# Public
#---

@click.group(
    name     = 'crupydsltester',
    commands = [
        crupydsltester_cli_unittest_entry,
    ],
)
@click.version_option()
def crupydsltester_cli_entry() -> None:
    """ Crupy DSL parser """
