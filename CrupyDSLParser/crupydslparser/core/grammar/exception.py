"""
crupydslparser.core.grammar.exception    - general grammar exception class
"""
__all__ = (
    'CrupyGrammarException',
)

from crupydslparser.core.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyGrammarException(CrupyDSLCoreException):
    """ general crupy grammar exception class """
