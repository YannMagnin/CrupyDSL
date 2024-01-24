"""
crupy.core.grammar._dsl.exception   - DSL exception class
"""
__all__ = [
    'CrupyGrammarDSLException',
]

from crupy.core.grammar.exception import CrupyGrammarException

#---
# Public
#---

class CrupyGrammarDSLException(CrupyGrammarException):
    """ generic DSL exception class """
