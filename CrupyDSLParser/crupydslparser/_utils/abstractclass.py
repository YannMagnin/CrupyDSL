"""
crupydslparser._utils.abstractclass - custom abstract class decorator
"""
__all__ = [
    'crupyabstractclass',
]
from typing import Any

from crupydslparser.exception import CrupyDSLCoreException

#---
# Internals
#---

# Allow too few public methods
# pylint: disable=locally-disabled,R0903

class _CrupyAbstractClass():
    """ custom abstract class implementation
    """
    hook_init_book: dict[str,Any] = {}

    def __init_crupy_common__(
        self,
        class_type: str,
        args: list[Any],
        kwargs: dict[str,Any],
    ) -> None:
        """ special object constructor hook

        When an class use the `crupyabstractclass` decorator a special
        unique method is created that invoke this magical constructor with
        the current object being initialised, the targeted class that need
        to be constructed (and that have a `crupyabstractclass` decorator)
        and user-provided arguments for the "original" constructor.

        We will simply check if the current object being initialized is the
        targeted class (wich mean that the user try to instanciate our
        abstract class which is not allowed) and branch to the original
        constructor if exists.

        We dissociate the current object and the target class to properly
        support the `super()` mechanism that do not allow to know at which
        step of the MRO we are.
        """
        if self.__class__.__name__ == class_type:
            raise CrupyDSLCoreException(
                f"class '{self.__class__.__name__}' cannot be instanciated "
                'since this class has been declared as crupyabstactclass'
            )
        if class_type not in _CrupyAbstractClass.hook_init_book:
            raise CrupyDSLCoreException(
                f"class '{class_type}' has not been registered o(x_x)o"
            )
        hook_init = _CrupyAbstractClass.hook_init_book[class_type]
        if hook_init is not None:
            hook_init(self, *args, **kwargs)

#---
# Public
#---

# Allow the use of `exec` builtin
# pylint: disable=locally-disabled,W0122

def crupyabstractclass(origin_class: Any) -> Any:
    """ decorator to ensure that the class will never be instanciated

    As quickly explained in the special constructor in _CrupyAbstractClass,
    we cannot have a "mutual/centralised" constructor that hook the original
    one because of the `super()` mechanism and MRO limitation.

    Since the `super().__init__()` builtin look-up the MRO to fetch the
    next construtor to invoke and provide the current object as a `self`
    argument we cannot guess (?) at which step of the MRO we are. And this
    limitation do not allow us to proper resolve multiple inheritance
    classes.

    So, we create a "dynamic" function that will hook our hook :]

    This allow to statically register the class name that is used to quickly
    find the original constructor and dispel ambigius shenanigans for the
    target class guessing.
    """
    def wrap(origin_class: Any) -> Any:
        _CrupyAbstractClass.hook_init_book[
            origin_class.__name__
        ] = origin_class.__init__
        hook_init_func = f"__init_{origin_class.__name__}_hook"
        exec(
            f"def {hook_init_func}(self, *args, **kwargs):\n"
             '    return _CrupyAbstractClass.__init_crupy_common__(\n'
             '        self        = self,\n'
            f"        class_type  = '{origin_class.__name__}',\n"
             '        args        = args,\n'
             '        kwargs      = kwargs,\n'
             '    )'
        )
        origin_class.__init__ = locals()[hook_init_func]
        return origin_class
    if origin_class is None:
        return wrap
    return wrap(origin_class)
