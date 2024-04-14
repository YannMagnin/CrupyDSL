"""
crupydslparser.parser._lexer._operation._base - Lexer operation abstraction
"""
__all__ = [
    'CrupyLexerOpBase',
]
from typing import Any
from abc import ABC, abstractmethod

from crupydslparser.parser._lexer.exception import CrupyLexerException
from crupydslparser.parser import (
    CrupyParserBase,
    CrupyParserNodeBase,
)

#---
# Public
#---

# allow too few public methods
# pylint: disable=locally-disabled,R0903
class CrupyLexerOpBase(ABC):
    """ Lexer capture operation
    """

    #---
    # Magic mechanism used to ensure class formalism
    #---

    def __init_subclass__(cls, /, **kwargs: dict[str,Any]) -> None:
        """ guess token name based on class name
        """
        if (
                cls.__name__.find('CrupyLexerOp') != 0
            and cls.__name__.find('_CrupyLexerOp') != 0
        ):
            raise CrupyLexerException(
                f"Malformated lexer operation class name '{cls.__name__}'"
            )

    #---
    # Magic operation
    #---

    @abstractmethod
    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ internal core operation code
        """
