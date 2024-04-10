"""
crupy.parser._stream.exception  - crupy stream general exception
"""
__all__ = [
    'CrupyStreamException',
]

from crupydslparser.parser.exception import CrupyParserException

#---
# Public
#---

class CrupyStreamException(CrupyParserException):
    """ crupy stream general exception class """
