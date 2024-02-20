"""
crupydslparser.core._lexer._assert._base    - Lexer assert abstraction
"""
__all__ = [
    'CrupyLexerAssertBase',
]
from typing import Dict, Any
from abc import ABC, abstractmethod

from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core.parser._base import CrupyParserBase

#---
# Public
#---

class CrupyLexerAssertBase(ABC):
    """ Lexer assert operation
    """

    #---
    # Magic mechanism used to auto-generate class information
    #---

    _name: str  = ''

    def __init_subclass__(cls, /, **kwargs: Dict[str,Any]) -> None:
        """ guess token name based on class name
        """
        super().__init_subclass__(**kwargs)
        if cls.__name__.find('CrupyLexerAssert') != 0:
            raise CrupyLexerException(
                f"Malformated lexer assert class name '{cls.__name__}'"
            )
        cls._name = cls.__name__[12:].lower()

    #---
    # Pulic methods
    #---

    @abstractmethod
    def __call__(self, stream: CrupyParserBase) -> bool:
        pass

    #---
    # Public property
    #---

    @property
    def name(self) -> str:
        """ return the lexer name """
        return self._name
