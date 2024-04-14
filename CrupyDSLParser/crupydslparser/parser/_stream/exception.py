"""
crupy.parser._stream.exception  - crupy stream general exception
"""
__all__ = [
    'CrupyStreamException',
]

from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

class CrupyStreamException(CrupyParserBaseException):
    """ crupy stream general exception class """
