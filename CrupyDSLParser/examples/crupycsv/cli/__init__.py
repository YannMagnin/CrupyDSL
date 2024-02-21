"""
crupycsv.cli    - crupycsv CLI entry
"""
__all__ = [
    'crupycsv_cli_entry',
]
import click

from crupycsv.cli.tests import crupycsv_cli_tests_entry

#---
# Public
#---

@click.group(
    'crupoycsv',
    commands = [
        crupycsv_cli_tests_entry,
    ],
)
def crupycsv_cli_entry() -> None:
    """ CSV parser using CrupyDSLParser """
