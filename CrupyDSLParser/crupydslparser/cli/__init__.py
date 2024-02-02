"""
crupydslparser.cli   - Crupy CLI entry
"""
__all__ = [
    'crupydslparser_cli_entry',
]
import click

from crupydslparser.cli.doctor import crupydslparser_cli_doctor_entry

#---
# Public
#---

@click.group(
    name     = 'crupydslparser',
    commands = [
        crupydslparser_cli_doctor_entry,
    ],
)
def crupydslparser_cli_entry() -> None:
    """ Crupy DSL parser """
