"""
crupydsl.parser._lexer._operation._base - Lexer operation abstraction
"""
__all__ = [
    'CrupyDSLLexerOpBase',
]
from abc import abstractmethod

from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser.node import CrupyDSLParserNodeBase
from crupydsl._utils import (
    crupyabstractclass,
    crupynamedclass,
)

#---
# Public
#---

# allow too few public methods
# pylint: disable=locally-disabled,R0903

@crupyabstractclass
@crupynamedclass(
    generate_type   = True,
    regex           = '^(_)?CrupyDSLLexerOp(?P<type>([0-9]*[A-Z][a-z]*)+)$',
)
class CrupyDSLLexerOpBase():
    """ Lexer capture operation
    """

    #---
    # Magic operation
    #---

    @abstractmethod
    def __call__(self, parser: CrupyDSLParserBase) -> CrupyDSLParserNodeBase:
        """ internal core operation code
        """

    #---
    # Public (generic) methods
    #---

    @abstractmethod
    def debug_show(self, indent: int = 0) -> str:
        """ display a generic information
        """
