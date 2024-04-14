"""
crupydslparser.parser.node  - parser node base class
"""
from __future__ import annotations
__all__ = [
    'CrupyParserNodeBase',
]
from typing import Any

from crupydslparser.parser.exception import CrupyParserBaseException
from crupydslparser.parser._stream.context import CrupyStreamContext
from crupydslparser._utils import (
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
    regex           = '^CrupyParserNode(?P<type>([A-Z][a-z]+)+)$',
    error           = 'malformated parser node subclass',
)
class CrupyParserNodeBase():
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
    `context` should be of type `CrupyStreamContext` and it's required
    for the creation of the object
    """
    type: str
    parent_node: CrupyParserNodeBase|None
    context: CrupyStreamContext

    def __init__(self, /, **_: Any) -> None:
        """ special initialisation routine

        A lot of magic as been involved before we branch to this
        contructor.

        First, a check has been performed on the class name to ensure that
        subclass have the same name and to deduce the "class" type
        attribute (e.g. `CrupyParserNodeBaseLexerSeq` -> type=`lexer_seq`)
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
        if not self.context:
            if not self.parent_node:
                raise CrupyParserBaseException(
                    'Missing \'context\' declaration for '
                    f"'{type(self).__name__}'"
                )
            self.context = self.parent_node.context
