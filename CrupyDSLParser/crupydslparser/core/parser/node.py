"""
crupydslparser.core.parser.node     - parser node base class
"""
__all__ = [
    'CrupyParserNode',
]
from typing import Any, get_origin

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

        * `type`    : node type
        * `context` : stream context (which contain cursor information)

    We also need that the `name` attribute should not be able to be modified
    "on-the-fly" (no assignment possible) and thus, the `context` should
    be of type `CrupyStreamContext` and it's required for the creation of
    the object
    """
    # since this constructor is pretty huge, allow too many branches
    # pylint: disable=locally-disabled,R0912
    def __init__(self, /, **kwargs: Any) -> None:
        """ special initialisation routine

        @note
        - We use `typing.get_origin()` to magically check if the annotated
            variable is of type `typing.*` information which cannot be used
            with `isinstance()` because it will raise the `TypeError`
            exception
        - For now, ignore `typing` module import typing check
        """
        if self.__class__.__name__.find('CrupyParserNode') != 0:
            raise CrupyParserException(
                'Malformed parser node class name '
                f"'{self.__class__.__name__}'"
            )
        self._type = ''
        for letter in self.__class__.__name__[15:]:
            if self._type and letter.isupper():
                self._type += '_'
            self._type += letter.lower()
        parent_node: Any = None
        cls_annotations = self.__class__.__annotations__
        cls_annotations['context'] = CrupyStreamContext
        for item in kwargs.items():
            try:
                if item[0] == 'parent_node':
                    if not isinstance(item[1], CrupyParserNode):
                        raise CrupyParserException(
                            'Given `parent_node` type mismatch '
                            f"'{type(item[1])}' != CrupyParserNode"
                        )
                    parent_node = item[1]
                    continue
                if item[0] not in cls_annotations:
                    raise CrupyParserException(
                        f"Unable to assign class property '{item[0]}' for "
                        f"parser node subclass '{type(self)}'"
                    )
                type_info = cls_annotations[item[0]]
                if not get_origin(type_info):
                    if not isinstance(item[1], type_info):
                        raise CrupyParserException(
                            f"{type(self)}: 'context' attribute type"
                            f"mismatch ({type(item[1])})"
                        )
                else:
                    # (todo) : proper handle typing information
                    # (todo) : use `typing.get_args()` to validate types
                    pass
            except TypeError as err:
                raise CrupyParserException(
                    f"{type(self)}: unable to validate the argument type "
                    f"({type(item[1])}) -> ({err})"
                ) from err
            setattr(self, item[0], item[1])
        if not getattr(self, 'context', None):
            if not parent_node:
                raise CrupyParserException(
                    f"Missing 'context' declaration for '{type(self)}'"
                )
            setattr(self, 'context', parent_node.stream_context)
        self._stream_context: CrupyStreamContext = getattr(
            self,
            'context',
        )

    #---
    # Magic operation
    #---

    def __str__(self) -> str:
        """ generate the string information about the object
        """
        content = f"<{self.__class__.__name__}("
        attributes = ['type'] + list(self.__class__.__annotations__)
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
        try:
            return getattr(self, key)
        except AttributeError as err:
            raise CrupyParserException(f"{err}") from err

    def __getattr__(self, name: str) -> Any:
        """ return the attribute `name`

        @note
        We are constraint to raise `AttributeError` if the attribute `name`
        is not found, otherwise the `getattr(obj, key, default)` will never
        return the default value
        """
        if name in self.__dict__:
            return self.__dict__[name]
        if name in self.__class__.__dict__:
            return self.__class__.__dict__[name]
        raise AttributeError(
            f"Unable to fetch the attribute '{name}' for the class "
            f"{self.__class__.__name__}"
        )

    #---
    # Public property
    #---

    @property
    def type(self) -> str:
        """ return the node type """
        return self._type

    @property
    def stream_context(self) -> CrupyStreamContext:
        """ return the stream context """
        if not self._stream_context:
            raise CrupyParserException('No stream context available')
        return self._stream_context
