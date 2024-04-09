"""
crupydslparser.cli.unittest     - unittest framework
"""
__all__ = [
    'crupydslparser_cli_unittest_entry',
]
from typing import NoReturn, Optional
import sys

import click

from crupydslparser.core.unittest import CrupyUnittestBase

#---
# Public
#---

@click.command('unittest')
@click.option(
    '-l', '--list', 'disp_list',
    is_flag     = True,
    required    = False,
    help        = 'only display availalbe test file'
)
@click.option(
    '-t', '--target', 'target_tests',
    required    = False,
    multiple    = True,
    help        = 'only execute target tests',
)
def crupydslparser_cli_unittest_entry(
    disp_list:      bool,
    target_tests:   Optional[list[str]],
) -> NoReturn:
    """ Unittest CLI entry
    """
    if disp_list:
        for test_name in CrupyUnittestBase.iter_tests():
            print(f"- {test_name}")
        sys.exit(0)
    if target_tests:
        target_tests = [y for x in target_tests for y in x.split(',')]
    CrupyUnittestBase.run_tests(target_tests)
    sys.exit(0)
