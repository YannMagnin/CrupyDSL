"""
crupydslparser.core._lexer._assert._base    - Lexer assert abstraction
"""
__all__ = (
    'CrupyLexerAssertBase',
)
from typing import Any
from abc import ABC, abstractmethod

from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core.parser import CrupyParserBase

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

    def __init_subclass__(cls, /, **kwargs: dict[str,Any]) -> None:
        """ guess token name based on class name
        """
        super().__init_subclass__(**kwargs)
        if cls.__name__.find('CrupyLexerAssert') != 0:
            raise CrupyLexerException(
                f"Malformated lexer assert class name '{cls.__name__}'"
            )
        cls._name = ''
        for letter in cls.__name__[16:]:
            if cls._name and letter.isupper():
                cls._name += '_'
            cls._name += letter.lower()

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
