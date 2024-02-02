"""
crupydslparser.cli.doctor.dsl    - Crupy DSL doctor CLI interface
"""
__all__ = [
    'crupydslparser_cli_doctor_dsl_entry',
]
from typing import NoReturn
import sys

import click

#---
# Public
#---

@click.command('dsl')
def crupydslparser_cli_doctor_dsl_entry() -> NoReturn:
    """ Crupy DSL parser doctor interface
    """
    sys.exit(0)
