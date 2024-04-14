"""
crupydslparser._utils.dataclass - custom dataclass implementation
"""
__all__ = [
    'crupydataclass',
]
from typing import Any

from crupydslparser.exception import CrupyDSLCoreException
from crupydslparser._utils.typing import crupy_typing_check

#---
# Internals
#---

class _CrupyDataclass():
    """ custom dataclass implementation

    This class is a bit exotic because we want a lazy attribute description
    for subclass declaration. The idea is to have the same declaration
    mechanism than CPython's dataclasses : simply describe class attribute
    with typing information and the object will provide atrribute and error
    if missing initialiser is detected.

    A detail that description with underscore will be ignored and en error
    will be raised if initialised through the object initialisation
    """
    hook_init_book: dict[str,Any] = {}

    def __init__(self, /, **kwargs: Any) -> None:
        cls_annotations = self.__class__.__annotations__
        for item in kwargs.items():
            if item[0] not in cls_annotations:
                raise CrupyDSLCoreException(
                    f"Unable to assign class property '{item[0]}' for "
                    f"parser node subclass '{type(self)}'"
                )
            if not crupy_typing_check(item[1], cls_annotations[item[0]]):
                raise CrupyDSLCoreException(
                    f"{type(self)}: unable to validate the argument "
                    f"'{item[1]} with type {type(item[1]).__name__}, must"
                    f"be of type {str(cls_annotations[item[0]])}"
                )
            setattr(self, item[0], item[1])
        # (todo) : check missing attribute definition
        if self.__class__.__name__ in _CrupyDataclass.hook_init_book:
            _CrupyDataclass.hook_init_book[self.__class__.__name__](self)

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
            raise CrupyDSLCoreException(f"{err}") from err

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
# Public
#---

def crupydataclass(
    origin_class: Any       = None,
    enable_getattr: bool    = True,
    enable_getitem: bool    = True,
    enable_repr: bool       = True,
) -> Any:
    """ decorator to convert fields defined in the class to properties

    If `enable_getattr` is True, the current implementation of
    `__getattr__` will be overriden. Same for `enable_getitem` which replace
    the `__getitem__` and `enable_repr` for `__repr__` and `__str__`

    Also note that the `__init__` method will be hooked and involved at the
    end of the new one (see `_CrupyDataclass.__init__`)
    """
    def wrap(origin_class: Any) -> Any:
        _CrupyDataclass.hook_init_book[
            origin_class.__name__
        ] = origin_class.__init__
        origin_class.__init__ = _CrupyDataclass.__init__
        if enable_getitem:
            origin_class.__getitem__ = _CrupyDataclass.__getitem__
        if enable_getattr:
            origin_class.__getattr__ = _CrupyDataclass.__getattr__
        if enable_repr:
            origin_class.__repr__ = _CrupyDataclass.__repr__
            origin_class.__str__ = _CrupyDataclass.__str__
        return origin_class
    if origin_class is None:
        print('ORIGIN_CLASS IS NONE, RETURN WRAPPER')
        return wrap
    print('ORIGIN_CLASS VALID, INVOKE WRAPPER')
    return wrap(origin_class)
