"""
crupydslparser.parser._lexer._operation._base - Lexer operation abstraction
"""
__all__ = [
    'CrupyLexerOpBase',
]
from abc import abstractmethod

from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser._utils import (
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
    regex           = '^(_)?CrupyLexerOp(?P<type>([A-Z][a-z]+)+)$',
)
class CrupyLexerOpBase():
    """ Lexer capture operation
    """

    #---
    # Magic operation
    #---

    @abstractmethod
    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ internal core operation code
        """
