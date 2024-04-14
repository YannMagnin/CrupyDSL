"""
crupy.parser._stream.exception  - crupy stream general exception
"""
__all__ = [
    'CrupyParserStreamException',
]

from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

class CrupyParserStreamException(CrupyParserBaseException):
    """ crupy stream general exception class """
