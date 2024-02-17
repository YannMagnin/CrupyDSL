"""
crupydslparser.core._lexer._lexer    - Lexer abstraction
"""
__all__ = [
    'CrupyLexer',
]
from typing import Dict, Any
from abc import ABC, abstractmethod

from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core._lexer._token import CrupyLexerToken
from crupydslparser.core._parser._base import CrupyParserBase

#---
# Public
#---

class CrupyLexer(ABC):
    """ Lexer abstraction
    """

    #---
    # Magic mechanism used to auto-generate class information
    #---

    _name: str  = ''

    def __init_subclass__(cls, /, **kwargs: Dict[str,Any]) -> None:
        """ guess token name based on class name
        """
        if cls.__name__.find('CrupyLexerToken') == 0:
            raise CrupyLexerException(
                f"Malformated token class name '{cls.__name__}'"
            )
        cls._name = cls.__name__[15:].lower()

    #---
    # Pulic methods
    #---

    @abstractmethod
    def __call__(self, stream: CrupyParserBase) -> CrupyLexerToken|None:
        pass

    #---
    # Public property
    #---

    @property
    def name(self) -> str:
        """ return the lexer name """
        return self._name
