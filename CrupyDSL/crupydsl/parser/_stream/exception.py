"""
crupy.parser._stream.exception  - crupy stream general exception
"""
__all__ = [
    'CrupyDSLStreamException',
]

from crupydsl.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyDSLStreamException(CrupyDSLCoreException):
    """ crupy stream general exception class """
