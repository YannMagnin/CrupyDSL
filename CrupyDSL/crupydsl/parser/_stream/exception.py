"""
crupy.parser._stream.exception  - crupy stream general exception
"""
__all__ = [
    'CrupyStreamException',
]

from crupydsl.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyStreamException(CrupyDSLCoreException):
    """ crupy stream general exception class """
