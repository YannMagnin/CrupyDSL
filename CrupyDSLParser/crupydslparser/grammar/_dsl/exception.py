"""
crupydslparser.grammar._dsl.exception   - DSL exception class
"""
__all__ = [
    'CrupyDSLException',
]

from crupydslparser.grammar.exception import CrupyGrammarException

#---
# Public
#---

class CrupyDSLException(CrupyGrammarException):
    """ generic DSL exception class """
