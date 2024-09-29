"""
crupydslparser.grammar._dsl._parser.between     - DSL between hook
"""
__all__ = [
    'dsl_between_hook',
    'dsl_between_hook_error',
]
from typing import NoReturn

from crupydslparser.parser import CrupyParserNodeBase
from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

def dsl_between_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle "eol" node
    """
    raise AssertionError('Not implemented')

def dsl_between_hook_error(
    err: CrupyParserBaseException,
) -> NoReturn:
    """ string error hook
    """
    raise AssertionError('Not implemented')
