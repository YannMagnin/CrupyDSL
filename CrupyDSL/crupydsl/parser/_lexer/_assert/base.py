"""
crupydsl.parser._lexer._assert._base  - Lexer assert abstraction
"""
__all__ = [
    'CrupyDSLLexerAssertBase',
]
from typing import Any
from abc import abstractmethod

from crupydsl.parser import CrupyDSLParserBase
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
    regex           = '^(_)?CrupyDSLLexerAssert(?P<type>([A-Z][a-z]+)+)$',
)
class CrupyDSLLexerAssertBase():
    """ Lexer assert operation
    """

    #---
    # Magic operation
    #---

    @abstractmethod
    def __call__(self, stream: CrupyDSLParserBase) -> bool:
        """ internal core operation code
        """

    def __getattribute__(self, name: Any, /) -> Any:
        """ workaround for mypy and pylint """
        return super().__getattribute__(name)

    #---
    # Public methods
    #---

    @abstractmethod
    def debug_show(self, indent: int = 0) -> str:
        """ display a generic information
        """
