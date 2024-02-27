"""
crupydslparser.core._lexer._operation._base - Lexer operation abstraction
"""
__all__ = [
    'CrupyLexerOpBase',
]
from typing import Dict, Any
from abc import ABC, abstractmethod

from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core.parser.node import CrupyParserNode
from crupydslparser.core.parser import CrupyParserBase

#---
# Public
#---

class CrupyLexerOpBase(ABC):
    """ Lexer capture operation
    """

    #---
    # Magic mechanism used to auto-generate class information
    #---

    _name: str  = ''

    def __init_subclass__(cls, /, **kwargs: Dict[str,Any]) -> None:
        """ guess token name based on class name
        """
        if cls.__name__[0] == '_':
            return
        if cls.__name__.find('CrupyLexerOp') != 0:
            raise CrupyLexerException(
                f"Malformated lexer operation class name '{cls.__name__}'"
            )
        cls._name = cls.__name__[12:].lower()

    #---
    # Pulic methods
    #---

    @abstractmethod
    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode|None:
        pass

    #---
    # Public property
    #---

    @property
    def name(self) -> str:
        """ return the lexer name """
        return self._name
