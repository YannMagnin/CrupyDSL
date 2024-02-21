"""
crupydsl.cli.tests  - crupycsv tests CLI entry
"""
__all__ = [
    'crupycsv_cli_tests_entry',
]
from typing import NoReturn
import sys

import click

from crupycsv._tests._parser.field import csv_test_parser_field
from crupycsv._parser import CSV_PARSER_OBJ

#---
# Public
#---

@click.command('tests')
def crupycsv_cli_tests_entry() -> NoReturn:
    """ execute all tests """
    csv_test_parser_field(CSV_PARSER_OBJ)
    sys.exit(0)
