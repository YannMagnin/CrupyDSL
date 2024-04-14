"""
crupydslparser._utils.namedclass - custom named class decorator
"""
__all__ = [
    'crupynamedclass',
]
from typing import Any, Optional
import re

from crupydslparser.exception import CrupyDSLCoreException

#---
# Internals
#---

# Allow too few public methods and too many arguments
# pylint: disable=locally-disabled,R0903,R0913

class _CrupyNamedClass():
    """ custom named class implementation
    """
    hook_init_book: dict[str,Any] = {}

    def __init_crupy_subclass__(
        self,
        class_origin: str,
        generate_type: bool,
        regex: Any,
        error: Optional[str],
        args: list[Any],
        kwargs: dict[str,Any],
    ) -> None:
        """ special constructor
        """
        class_name = self.__class__.__name__
        if not (info := re.match(regex, class_name)):
            if not error:
                error  = f"subclass '{self.__class__.__name__}' is "
                error += f"malformated to be compliant with {class_origin}"
            raise CrupyDSLCoreException(error)
        if generate_type:
            if 'type' not in info.groupdict():
                raise CrupyDSLCoreException(
                    'Unable to generate the \'type\' information for the '
                    f"subclass '{self.__class__.__name__}' because the "
                    f"given regex for all subclass of '{class_origin}' do "
                    'not provide the \'type\' group'
                )
            class_type = ''
            for char in info['type']:
                if class_type and char.isupper():
                    class_type += '_'
                class_type += char.lower()
            # (todo) : correct property behaviour
            # (todo) : check if the attribute 'type' already exists
            setattr(self, 'type', class_type)
        if class_origin not in _CrupyNamedClass.hook_init_book:
            raise CrupyDSLCoreException(
                f"internal error: class '{class_type}' has not been "
                'registered o(x_x)o'
            )
        hook_init = _CrupyNamedClass.hook_init_book[class_origin]
        if hook_init is not None:
            hook_init(self, *args, **kwargs)

#---
# Public
#---

# Allow the use of `exec` builtin
# pylint: disable=locally-disabled,W0122

def crupynamedclass(
    origin_class: Any    = None,
    regex: str           = '',
    generate_type: bool  = True,
    error: Optional[str] = None,
) -> Any:
    """ decorator to add extra class name check befor construction
    """
    def wrap(origin_class: Any) -> Any:
        # (todo) : raise error if not regex is provided
        _CrupyNamedClass.hook_init_book[
            origin_class.__name__
        ] = origin_class.__init__
        hook_init_func = f"__init_named_{origin_class.__name__}_hook"
        exec(
            f"def {hook_init_func}(self, *args, **kwargs):\n"
             '    _CrupyNamedClass.__init_crupy_subclass__(\n'
             '        self          = self,\n'
            f"        class_origin  = '{origin_class.__name__}',\n"
            f"        generate_type = {generate_type},\n"
            f"        regex         = '{regex}',\n"
            f"        error         = '{error}',\n"
             '        args          = args,\n'
             '        kwargs        = kwargs,\n'
             '    )'
        )
        origin_class.__init__ = locals()[hook_init_func]
        return origin_class
    if origin_class is None:
        return wrap
    return wrap(origin_class)
