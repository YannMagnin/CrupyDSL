"""
crupydslparser.core._dsl.exception   - DSL exception class
"""
__all__ = [
    'CrupyDSLException',
]

from crupydslparser.core.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyDSLException(CrupyDSLCoreException):
    """ generic DSL exception class """
