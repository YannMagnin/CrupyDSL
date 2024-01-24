"""
crupy.core.grammar.exception    - general grammar exception class
"""
__all__ = [
    'CrupyGrammarException',
]

from crupy.core.exception import CrupyException

#---
# Public
#---

class CrupyGrammarException(CrupyException):
    """ general crupy grammar exception class """
