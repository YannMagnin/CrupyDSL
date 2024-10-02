"""
crupydsl.parser._lexer._assert._base  - Lexer assert abstraction
"""
__all__ = [
    'CrupyLexerAssertBase',
]
from typing import Any
from abc import abstractmethod

from crupydsl.parser import CrupyParserBase
from crupydsl._utils import (
    crupyabstractclass,
    crupynamedclass,
)

#---
# Public
#---

@crupyabstractclass
@crupynamedclass(
    generate_type   = True,
    regex           = '^(_)?CrupyLexerAssert(?P<type>([A-Z][a-z]+)+)$',
)
class CrupyLexerAssertBase():
    """ Lexer assert operation
    """

    #---
    # Magic operation
    #---

    @abstractmethod
    def __call__(self, stream: CrupyParserBase) -> bool:
        """ internal core operation code
        """

    def __getattribute__(self, name: Any, /) -> Any:
        """ workaround for mypy and pylint """
        return super().__getattribute__(name)

    #---
    # Public methods
    #---

    @abstractmethod
    def show(self, indent: int = 0) -> str:
        """ display a generic information
        """
