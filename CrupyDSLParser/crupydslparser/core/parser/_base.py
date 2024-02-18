"""
crupydslparser.core._parser.base    - parser base class
"""
# @note
# Used as a workaround for the cyclic-import with the `CrupyLexer` class
from __future__ import annotations

__all__ = [
    'CrupyParserBase',
]
from typing import Dict, Optional, TYPE_CHECKING

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
        production_book:    Optional[Dict[str,CrupyLexer]] = None,
    ) -> None:
        self._stream: CrupyStream|None = None
        self._production_book: Dict[str,CrupyLexer] = {}
        if production_book:
            self._production_book = production_book

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

    def execute(self, production_name: str) -> CrupyParserNode|None:
        """ execute a particular production name
        """
        if production_name not in self._production_book:
            raise CrupyParserException(
                'Unable to find the primary production entry name '
                f"'{production_name}'"
            )
        return self._production_book[production_name](self)
