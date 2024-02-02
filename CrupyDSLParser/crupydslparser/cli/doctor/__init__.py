"""
crupydslparser.cli.doctor    - Doctor CLI entries
"""
__all__ = [
    'crupydslparser_cli_doctor_entry',
]
import click

from crupydslparser.cli.doctor.dsl import crupydslparser_cli_doctor_dsl_entry

#---
# Public
#---

@click.group(
    name     = 'doctor',
    commands = [
        crupydslparser_cli_doctor_dsl_entry,
    ],
)
def crupydslparser_cli_doctor_entry() -> None:
    """ Crupy DSL parser doctor interface """
