"""
crupydslparser.core._parser.base    - parser base class
"""
# @note
# Used as a workaround for the cyclic-import with the `CrupyLexer` class
from __future__ import annotations

__all__ = (
    'CrupyParserBase',
)
from typing import (
    Union, Optional, Literal, IO, Any, TYPE_CHECKING,
    cast,
)
from collections.abc import Callable

import typesentry

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
    from crupydslparser.core._lexer._operation._base import (
        CrupyLexerOpBase,
    )

#---
# Public
#---

class CrupyParserBase():
    """ Crupy parser class
    """
    def __init__(
        self,
        production_book: Optional[dict[str,CrupyLexerOpBase]] = None,
    ) -> None:
        self._stream: CrupyStream|None = None
        self._production_book: dict[str,CrupyLexerOpBase] = {}
        if production_book:
            self._production_book = production_book
        self._hook_postprocess_book: dict[
            str,
            list[Callable[[CrupyParserNode], CrupyParserNode]],
        ]= {}
        self._hook_error_book: dict[
            str,
            list[Callable[[str], None]],
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
    def production_book(self) -> dict[str,CrupyLexerOpBase]:
        """ return the current registered rules """
        return self._production_book

    #---
    # Internal methods
    #---

    def _execute_hook(
        self,
        target: str,
        production_name: str,
        *args: Any,
    ) -> CrupyParserNode:
        """ execute a hook if available
        """
        hook_book = getattr(self, f"_{target}_book")
        if production_name not in hook_book:
            if target == 'postprocess':
                return cast(CrupyParserNode, args[0])
            raise args[0]
        try:
            for hook in hook_book[production_name]:
                node = cast(CrupyParserNode, hook(*args))
            return node
        except Exception as err:
            if target == 'error':
                raise err
            raise CrupyParserException(
                f"{args[0].stream_context.traceback()}\n"
                '\n'
                f"Exception durring '{hook.__name__}' hook, abort\n"
                f"{err}"
            ) from err

    #---
    # Public methods
    #---

    def execute(self, production_name: str) -> CrupyParserNode:
        """ execute a particular production name
        """
        if production_name not in self._production_book:
            raise CrupyParserException(
                'Unable to find the primary production entry name '
                f"'{production_name}'"
            )
        try:
            node = self._production_book[production_name](self)
        except CrupyParserException as err:
            self._execute_hook('error', production_name, err)
        return self._execute_hook('postprocess', production_name, node)

    def register_stream(self, stream: CrupyStream|IO[str]|str) -> None:
        """ register a stream
        """
        if isinstance(stream, CrupyStream):
            self._stream = stream
        else:
            self._stream = CrupyStream.from_any(stream)

    def register_hook(
        self,
        target: Literal['postprocess','error'],
        production_name: str,
        hook: Union[
            Callable[[CrupyParserNode],CrupyParserNode],
            Callable[[CrupyParserNode],None],
        ],
    ) -> None:
        """ register a new hook for a production
        """
        if production_name not in self._production_book:
            raise CrupyParserException(
                'Unable to find the primary production entry name '
                f"'{production_name}'"
            )
        if target not in ['error', 'postprocess']:
            raise CrupyParserException(
                'Unable to register the hook for the production '
                f"'{production_name}' because you only can select 'error' "
                'postprocess'
            )
        type_info = {
            'error'       : Callable[[CrupyParserNode],None],
            'postprocess' : Callable[[CrupyParserNode],CrupyParserNode],
        }[target]
        if not typesentry.Config.is_type(hook,type_info):
            raise CrupyParserException(
                f"Unable to register the hook {hook.__name__} because "
                f"its signature do not match the '{target}' hook "
                f"signature {str(type_info)[7:]}"
            )
        hook_book = getattr(self, f"_{target}_book")
        if production_name not in hook_book:
            hook_book[production_name] = []
        hook_book[production_name].append(hook)
