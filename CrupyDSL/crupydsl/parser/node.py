"""
crupydsl.parser.node  - parser node base class
"""
from __future__ import annotations
__all__ = [
    'CrupyDSLParserNodeBase',
]
from typing import Any

from crupydsl.exception import CrupyDSLCoreException
from crupydsl.parser._stream.context import CrupyDSLStreamContext
from crupydsl._utils import (
    crupydataclass,
    crupyabstractclass,
    crupynamedclass,
)

#---
# Public
#---

# Allow too few public methods
# pylint: disable=locally-disabled,R0903

@crupydataclass
@crupyabstractclass
@crupynamedclass(
    generate_type   = True,
    regex           = '^(_)*CrupyDSLParserNode(?P<type>([A-Z][a-z]+)+)$',
    error           = 'malformated parser node subclass',
)
class CrupyDSLParserNodeBase():
    """ Crupy parser node abstraction

    This class is a bit exotic because we want a lazy attribute description
    for subclass declaration. The idea is to have the same declaration
    mechanism than CPython's dataclasses : simply describe class attribute
    with typing information

    But, each node should have default information that we want to
    "auto-magically" generate :

        * `type`    : node type
        * `context` : stream context (which contain cursor information)

    We also need that the `name` attribute should not be able to be
    modified "on-the-fly" (no assignment possible) and thus, the
    `context` should be of type `CrupyDSLStreamContext` and it's required
    for the creation of the object
    """
    type: str
    parent_node: CrupyDSLParserNodeBase|None
    context: CrupyDSLStreamContext

    def __init__(self, /, **_: Any) -> None:
        """ special initialisation routine

        A lot of magic as been involved before we branch to this
        contructor.

        First, a check has been performed on the class name to ensure that
        subclass have the same name and to deduce the "class" type
        attribute (e.g. `CrupyDSLParserNodeBaseLexerSeq` -> type=`lexer_seq`)
        (this magical behaviour is provided by `crupynamedclass` decorator)

        After that, a check is performed to ensur that the current class is
        not directly used as a node object (behaviour provided by
        `crupyabstractclass`)

        And a huge handling has been performed to match annotaction (e.g.
        class attribute `type`, `parent_node` and `context` here) and user
        provided arguments to construct the node. (provided by
        `crupydataclass`).

        So, when this constructor is involved all constructor argument has
        already been handled. The only thing that we should care, is to
        ensure that the context has been provided.
        """
        if not getattr(self, 'context', None):
            if not (node := getattr(self, 'parent_node', None)):
                raise CrupyDSLCoreException(
                    'Missing \'context\' declaration for '
                    f"'{type(self).__name__}'"
                )
            setattr(self, 'context', node.context)

    def __getattr__(self, index: str) -> Any:
        """ workaround to trick pylint

        Since we use a lot of magic to generate this class, pylint is not
        able to understand what we do with all of the class decorator. So,
        we have a lot of "no-member" false-possitive, but if we provide this
        magic method, pylint do not throw the error.
        """

    #---
    # Internals
    #---

    def __show_tweak(self, obj: Any, indent: int) -> str:
        """ try to handle pretty print for laest type has possible
        """
        if isinstance(obj, (CrupyDSLParserNodeBase, CrupyDSLStreamContext)):
            return f"{obj.show(indent)}"
        if isinstance(obj, str):
            return repr(obj)
        if isinstance(obj, list):
            padding0 = '    ' * (indent + 0)
            padding1 = '    ' * (indent + 1)
            content = f"[\t# {len(obj)} entries\n"
            for entry in obj:
                content += f"{padding1}"
                content += f"{self.__show_tweak(entry, indent + 1)},\n"
            content += f"{padding0}]"
            return content
        if isinstance(obj, dict):
            padding0 = '    ' * (indent + 0)
            padding1 = '    ' * (indent + 1)
            content = '{' + f"\t# {len(obj)} entries\n"
            for key, value in obj.items():
                content += f"{padding1}"
                content += f"{self.__show_tweak(key, indent + 1)} : "
                content += f"{self.__show_tweak(value, indent + 1)},\n"
            content += f"{padding0}" + '}'
            return content
        return str(obj)

    #---
    # Public methods
    #---

    def show(self, indent: int = 0) -> str:
        """ pretty print the AST (ignore attached parent information)

        @note
        - force `type` and `context` field to be first
        """
        padding0 = '    ' * (indent + 0)
        padding1 = '    ' * (indent + 1)
        content  = f"{type(self).__name__}(\n"
        for attr in ['type', 'context']:
            obj = getattr(self, attr)
            content += f"{padding1}{attr}\t= "
            content += f"{self.__show_tweak(obj, indent + 1)},\n"
        for attr in self.__dict__:
            if attr in ['type', 'context']:
                continue
            obj = getattr(self, attr)
            content += f"{padding1}{attr}\t= "
            content += f"{self.__show_tweak(obj, indent + 1)},\n"
        content += f"{padding0})"
        return content.expandtabs(4)

    def workaround_linter(self) -> None:
        """ this method do nothing

        This method has been implemented to remove generic warnings with
        pylint/mypy which require at least two public methods for a class. I
        know that we can remove theses warnings with some configuration
        flags, but I want to avoid at most of possible to indicate to the
        user "you need to properly configure your tools to work with my
        project".

        This is not acceptable, so yes, expose a fake symbol to avoid that
        """
