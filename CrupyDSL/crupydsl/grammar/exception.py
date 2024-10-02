"""
crupydsl.grammar.exception    - general grammar exception class
"""
__all__ = [
    'CrupyDSLGrammarException',
]

from crupydsl.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyDSLGrammarException(CrupyDSLCoreException):
    """ general crupy grammar exception class """
