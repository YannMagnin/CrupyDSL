"""
crupydslparser.core._lexer._token    - lexer token base class
"""
__all__ = [
    'CrupyLexerToken',
]
from typing import Dict, Any

from crupydslparser.core._lexer.exception import CrupyLexerException

#---
# Public
#---

class CrupyLexerToken():
    """ Crupy lexer token abstraction
    """

    #---
    # Magic mechanism used to auto-generate class information
    #---

    _name:       str  = ''
    _stream_ctx: None = None

    def __init_subclass__(cls, /, **kwargs: Dict[str,Any]) -> None:
        """ guess token name based on class name
        """
        if cls.__name__.find('CrupyLexerToken') != 0:
            raise CrupyLexerException(
                f"Malformated token class name '{cls.__name__}'"
            )
        cls._name = cls.__name__[15:].lower()
        cls._stream_ctx = None
        for item in kwargs.items():
            if hasattr(cls, item[0]):
                setattr(cls, item[0], item[1])
                continue
            raise CrupyLexerException(
                f"Unable to assign class property '{item[0]}' for "
                f"token subclass '{cls.__name__}'"
            )
        if not cls._stream_ctx:
            raise CrupyLexerException(
                f"Missing 'stream_ctx' declaration '{cls.__name__}'"
            )

    def __init__(self, *_: Any, **__: Any) -> None:
        pass

    #---
    # Public property
    #---

    @property
    def name(self) -> str:
        """ return the token name """
        return self._name

    @property
    def stream(self) -> None:
        """ return the stream context """
        return self._stream_ctx
