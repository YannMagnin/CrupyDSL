"""
crupydslparser.core.parser.node     - parser node base class
"""
__all__ = [
    'CrupyParserNode',
]
from typing import Any

from crupydslparser.core.parser.exception import CrupyParserException
from crupydslparser.core._stream.context import CrupyStreamContext

#---
# Public
#---

class CrupyParserNode():
    """ Crupy parser node abstraction

    This class is a bit exotic because we want a lazy attribute description
    for subclass declaration. The idea is to have the same declaration
    mechanism than CPython's dataclasses : simply describe class attribute
    with typing information

    But, each node should have default information that we want to
    "auto-magically" generate :

        * `name`        : node name
        * `stream_ctx`  : stream context (which contain cursor information)

    We also need that the `name` attribute should not be able to be modified
    "on-the-fly" (no assignment possible) and thus, the `stream_ctx` should
    be of type `CrupyStreamContext` and it's required for the creation of the
    object
    """
    def __init__(self, /, **kwargs: Any) -> None:
        """ special initialisation routine

        @note
        - We check if the `__origin__` field to magically check if the
            annotated is of type `typing.*` information which cannot be used
            with `isinstance()` because it will raise the `TypeError`
            exception
        """
        cls_annotations = self.__class__.__annotations__
        cls_annotations['stream_ctx'] = CrupyStreamContext
        for item in kwargs.items():
            if item[0] not in cls_annotations:
                raise CrupyParserException(
                    f"Unable to assign class property '{item[0]}' for "
                    f"parser node subclass '{type(self)}'"
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
                    raise CrupyParserException(
                        f"{type(self)}: stream_ctx attribute type"
                        f"mismatch ({type(item[1])})"
                    )
            except TypeError as err:
                raise CrupyParserException(
                    f"{type(self)}: unable to validate the argument type "
                    f"({type(item[1])}) -> ({err})"
                ) from err
            setattr(self, item[0], item[1])
        if not getattr(self, 'stream_ctx'):
            raise CrupyParserException(
                f"Missing 'stream_ctx' declaration for '{type(self)}'"
            )
        if self.__class__.__name__.find('CrupyParserNode') != 0:
            raise CrupyParserException(
                'Malformed parser node class name '
                f"'{self.__class__.__name__}'"
            )
        self._name = ''
        for letter in self.__class__.__name__[15:]:
            if self._name and letter.isupper():
                self._name += '_'
            self._name += letter.lower()
        self._stream_context: CrupyStreamContext = getattr(
            self,
            'stream_ctx',
        )

    #---
    # Magic operation
    #---

    def __str__(self) -> str:
        """ generate the string information about the object
        """
        content = f"<{self.__class__.__name__}("
        attributes = ['name'] + list(self.__class__.__annotations__)
        for i, keyname in enumerate(attributes):
            if i != 0:
                content += ', '
            content += f"{keyname}={getattr(self, keyname)}"
        content += ')>'
        return content

    def __repr__(self) -> str:
        """ small representation of the object """
        return self.__str__()

    def __getitem__(self, key: str) -> Any:
        """ return the 'key' attribute
        """
        if (attr := getattr(self, key, None)) is not None:
            return attr
        raise CrupyParserException(f"Unable to fetch the attribute '{key}'")

    #---
    # Public property
    #---

    @property
    def name(self) -> str:
        """ return the node name """
        return self._name

    @property
    def stream_context(self) -> CrupyStreamContext:
        """ return the stream context """
        if not self._stream_context:
            raise CrupyParserException('No stream context available')
        return self._stream_context
