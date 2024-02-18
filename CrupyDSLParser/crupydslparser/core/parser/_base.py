"""
crupydslparser.core._parser.base    - parser base class
"""
# @note
# Used as a workaround for the cyclic-import with the `CrupyLexer` class
from __future__ import annotations

__all__ = [
    'CrupyParserBase',
]
from typing import List, Dict, Optional, Callable, IO, TYPE_CHECKING

from crupydslparser.core._stream import CrupyStream
from crupydslparser.core.parser.exception import CrupyParserException
from crupydslparser.core.parser.node import CrupyParserNode

# @note : Design mistake
#
# We cannot import the `CrupyLexer` class since the magical `__call__()`
# method take a `CrupyParserBase` class as a its first argument (which is
# defined here. So, we are in a circular dependencies problem.
#
# For now, I use a combination of workarounds to by-pass this bad design
# limitation:
# - use the `TYPE_CHECKING` indicator to know if we are in checking mode
# - use the `annotations` import to allow "not well defined class"
# - import the missing `CrupyLexer` type
if TYPE_CHECKING:
    from crupydslparser.core._lexer._lexer import CrupyLexer

#---
# Public
#---

class CrupyParserBase():
    """ Crupy parser class
    """
    def __init__(
        self,
        production_book: Optional[Dict[str,CrupyLexer]] = None,
    ) -> None:
        self._stream: CrupyStream|None = None
        self._production_book: Dict[str,CrupyLexer] = {}
        if production_book:
            self._production_book = production_book
        self._hook_book: Dict[
            str,
            List[
                Callable[
                    [CrupyParserBase, CrupyParserNode],
                    CrupyParserNode,
                ],
            ],
        ]= {}

    #---
    # Public properties
    #---

    @property
    def stream(self) -> CrupyStream:
        """ return the current stream if any """
        if self._stream:
            return self._stream
        raise CrupyParserException('No stream registered')

    @property
    def production_book(self) -> Dict[str,CrupyLexer]:
        """ return the current registered rules """
        return self._production_book

    #---
    # Public methods
    #---

    def execute(
        self,
        production_name: str,
        stream: Optional[CrupyStream|IO[str]|str] = None,
    ) -> CrupyParserNode|None:
        """ execute a particular production name
        """
        if stream:
            if isinstance(stream, CrupyStream):
                self._stream = stream
            else:
                self._stream = CrupyStream.from_any(stream)
        if production_name not in self._production_book:
            raise CrupyParserException(
                'Unable to find the primary production entry name '
                f"'{production_name}'"
            )
        if not (node := self._production_book[production_name](self)):
            return None
        if production_name in self._hook_book:
            for hook in self._hook_book[production_name]:
                node = hook(self, node)
        return node

    def register_hook(
        self,
        production_name: str,
        handler: Callable[
            [CrupyParserBase, CrupyParserNode],
            CrupyParserNode,
        ],
    ) -> None:
        """ register a new hook for a production
        """
        if production_name not in self._production_book:
            raise CrupyParserException(
                'Unable to find the primary production entry name '
                f"'{production_name}'"
            )
        if production_name not in self._hook_book:
            self._hook_book[production_name] = []
        self._hook_book[production_name].append(handler)
