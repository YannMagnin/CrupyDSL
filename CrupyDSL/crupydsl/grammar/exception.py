"""
crupydsl.grammar.exception    - general grammar exception class
"""
__all__ = [
    'CrupyGrammarException',
]

from crupydsl.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyGrammarException(CrupyDSLCoreException):
    """ general crupy grammar exception class """
