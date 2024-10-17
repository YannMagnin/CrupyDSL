"""
crupydsl.grammar.exception    - general grammar exception class
"""
__all__ = [
    'CrupyDSLGrammarBaseException',
]

from crupydsl.exception import CrupyDSLCoreException
from crupydsl._utils import crupynamedclass

#---
# Public
#---

@crupynamedclass(
    generate_type   = True,
    regex           = \
        '^(_)*CrupyDSLGrammar(?P<type>([A-Z][a-z]+)+)Exception$',
)
class CrupyDSLGrammarBaseException(CrupyDSLCoreException):
    """ general crupy grammar exception class """
