"""
crupydslparser.core._lexer._token    - lexer token base class
"""
__all__ = [
    'CrupyLexerToken',
]
from typing import Any

from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core._stream.context import CrupyStreamContext

#---
# Public
#---

class CrupyLexerToken():
    """ Crupy lexer token abstraction
    """

    #---
    # Magic mechanism used to auto-generate class information
    #---

    _name: str  = ''

    def __init_subclass__(cls, /, **_: Any) -> None:
        """ guess token name based on class name
        """
        if cls.__name__.find('CrupyLexerToken') != 0:
            raise CrupyLexerException(
                f"Malformated token class name '{cls.__name__}'"
            )
        cls._name = cls.__name__[15:].lower()

    def __init__(self, /, **kwargs: Any) -> None:
        """ special initialisation routine
        """
        stream_context = None
        cls_annotations = self.__class__.__dict__['__annotations__']
        cls_annotations['stream_ctx'] = CrupyStreamContext
        for item in kwargs.items():
            if item[0] not in cls_annotations:
                raise CrupyLexerException(
                    f"Unable to assign class property '{item[0]}' for "
                    f"token subclass '{type(self)}'"
                )
            if not isinstance(item[1], cls_annotations[item[0]]):
                raise CrupyLexerException(
                    f"{type(self)}: stream_ctx attribute type"
                    f"mismatch ({type(item[1])})"
                )
            setattr(self, item[0], item[1])
        if not getattr(self, 'stream_ctx'):
            raise CrupyLexerException(
                f"Missing 'stream_ctx' declaration for '{type(self)}'"
            )
        self._stream_context = stream_context

    #---
    # Public property
    #---

    @property
    def name(self) -> str:
        """ return the token name """
        return self._name

    @property
    def stream_context(self) -> CrupyStreamContext:
        """ return the stream context """
        if not self._stream_context:
            raise CrupyLexerException('No stream context available')
        return self._stream_context
