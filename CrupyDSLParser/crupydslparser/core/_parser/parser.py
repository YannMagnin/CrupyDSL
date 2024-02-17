"""
crupydslparser.core._parser.parser  - high level parser export
"""
__all__ = [
    'CrupyParser',
]

from crupydslparser.core._parser._base import CrupyParserBase


#---
# Public
#---

class CrupyParser(CrupyParserBase):
    """ high-level crupy parser
    """
