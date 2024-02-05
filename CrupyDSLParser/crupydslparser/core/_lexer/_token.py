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

    This class is a bit exotic because we want a lazy attribute description
    for subclass declaration. The idea is to have the same declaration
    mechanism than CPython's dataclasses : simply describe class attribute
    with typing information

    But, token should have default information that we want to automatically
    generate :

        * `name`        : token name
        * `stream_ctx`  : stream context (which contain cursor information)

    We also need that the `name` attribute should not be able to be modified
    "on-the-fly" (no assignment possible) and thus, the `stream_ctx` should
    be of type `CrupyStreamContext` and is required for the creation of the
    object
    """
    def __init__(self, /, **kwargs: Any) -> None:
        """ special initialisation routine

        @note
        - We check if the `__origin__` field to magically check if the
            annotated is `typing.*` information which cannot be used with
            `isinstance()` because it will raise the `TypeError` exception
        """
        stream_context = None
        cls_annotations = self.__class__.__annotations__
        cls_annotations['stream_ctx'] = CrupyStreamContext
        for item in kwargs.items():
            if item[0] not in cls_annotations:
                raise CrupyLexerException(
                    f"Unable to assign class property '{item[0]}' for "
                    f"token subclass '{type(self)}'"
                )
            try:
                if not getattr(
                    cls_annotations[item[0]],
                    '__origin__',
                    None,
                ):
                    ok = isinstance(item[1], cls_annotations[item[0]])
                else:
                    ok = isinstance(
                        item[1],
                        cls_annotations[item[0]].__origin__,
                    )
                if not ok:
                    raise CrupyLexerException(
                        f"{type(self)}: stream_ctx attribute type"
                        f"mismatch ({type(item[1])})"
                    )
            except TypeError as err:
                raise CrupyLexerException(
                    f"{type(self)}: unable to validate the argument type "
                    f"({type(item[1])}) -> ({err})"
                ) from err
            setattr(self, item[0], item[1])
        if not getattr(self, 'stream_ctx'):
            raise CrupyLexerException(
                f"Missing 'stream_ctx' declaration for '{type(self)}'"
            )
        if self.__class__.__name__.find('CrupyLexerToken') != 0:
            raise CrupyLexerException(
                f"Malformed token class name '{self.__class__.__name__}'"
            )
        self._name = self.__class__.__name__[15:].lower()
        self._stream_context = stream_context

    #---
    # Magic operation
    #---

    def __getitem__(self, key: str) -> Any:
        """ return the 'key' attribute
        """
        if key in self.__dict__:
            return self.__dict__[key]
        raise CrupyLexerException(f"Unable to fetch the attribute '{key}'")

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
