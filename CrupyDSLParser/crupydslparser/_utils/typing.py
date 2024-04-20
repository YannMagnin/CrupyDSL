"""
crupydslparser._utils.typing    - custon typing abstraction
"""
__all__ = [
    'crupy_typing_check',
]
from typing import Any#, get_origin

#---
# Public
#---

def crupy_typing_check(_type_a: Any, _type_b: Any) -> bool:
    """ check typing match

    @note
    - We use `typing.get_origin()` to magically check if the annotated
        variable is of type `typing.*` information which cannot be used
        with `isinstance()` because it will raise the `TypeError`
        exception
    - For now, ignore `typing` module import typing check
    """
    #if not get_origin(type_a) and not get_origin(type_b):
    #    return isinstance(type_a, type_b)
    # (todo) : proper handle typing module
    # (todo) : use get_args() to proper match type info
    return True
