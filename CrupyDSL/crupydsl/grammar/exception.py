"""
crupydsl.grammar.exception    - general grammar exception class
"""
__all__ = [
    'CrupyDSLGrammarException',
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
class CrupyDSLGrammarException(CrupyDSLCoreException):
    """ general crupy grammar exception class """
