"""
crupy.core.stream.exception - crupy stream general exception
"""
__all__ = [
    'CrupyStreamException',
]

from crupydslparser.core.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyStreamException(CrupyDSLCoreException):
    """ crupy stream general exception class """
