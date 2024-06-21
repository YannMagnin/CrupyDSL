"""
crupyjson.cli.grammar   - grammar tests entry
"""
__all__ = [
    'crupyjson_cli_grammar_entry',
]
from typing import NoReturn
import sys

import click

from crupyjson._grammar import CrupyGrammarJSON

#---
# Public
#---

@click.command('grammar')
def crupyjson_cli_grammar_entry() -> NoReturn:
    """ grammar check
    """
    test = CrupyGrammarJSON()
    print(test)
    sys.exit(1)
