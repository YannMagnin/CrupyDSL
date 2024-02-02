"""
crupydslparser.core._lexer.exception     - lexer exception class
"""
__all__ = [
    'CrupyLexerException',
]

from crupydslparser.core.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyLexerException(CrupyDSLCoreException):
    """ Crupy lexer exception class """
