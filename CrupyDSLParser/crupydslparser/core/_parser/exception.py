"""
crupydslparser.core._parser.exception   - parser exception class
"""
__all__ = [
    'CrupyParserException',
]

from crupydslparser.core.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyParserException(CrupyDSLCoreException):
    """ Crupy parser exception class """
