"""
crupydslparser.cli.unittest     - unittest framework
"""
__all__ = [
    'crupydslparser_cli_unittest_entry',
]
from typing import NoReturn
import sys

import click

from crupydslparser.core.unittest import CrupyUnittestBase

#---
# Public
#---

@click.command('unittest')
def crupydslparser_cli_unittest_entry() -> NoReturn:
    """ Unittest CLI entry
    """
    CrupyUnittestBase.run_all_tests()
    sys.exit(0)
