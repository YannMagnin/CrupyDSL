"""
crupydslparser.core.unittest.exception  - unittest abstraction exception
"""
__all__ = (
    'CrupyUnittestException',
)

from crupydslparser.core.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyUnittestException(CrupyDSLCoreException):
    """ unittest general exception """
