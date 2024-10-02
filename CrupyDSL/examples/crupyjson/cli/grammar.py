"""
crupyjson.cli.grammar   - grammar tests entry
"""
__all__ = [
    'crupyjson_cli_grammar_entry',
]
from typing import Optional, NoReturn
from pathlib import Path
import sys

import click

from crupyjson._grammar import CrupyDSLGrammarJSON

#---
# Public
#---

@click.command('grammar')
@click.option(
    '-v', '--verbose',
    is_flag     = True,
    required    = False,
    help        = 'display grammar information',
)
@click.argument(
    'jsonfile',
    required    = False,
    type        = click.Path(
        exists      = True,
        file_okay   = True,
        dir_okay    = False,
        readable    = True,
        path_type   = Path,
    ),
)
def crupyjson_cli_grammar_entry(
    verbose: bool,
    jsonfile: Optional[Path],
) -> NoReturn:
    """ grammar check
    """
    test = CrupyDSLGrammarJSON()
    if not jsonfile or verbose:
        print(test.show())
    if jsonfile:
        print(test.parse(jsonfile))
    sys.exit(0)
