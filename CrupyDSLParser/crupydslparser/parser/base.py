"""
crupydslparser.parser.base  - parser base class
"""
# @note
# Used as a workaround for the cyclic-import with the `CrupyLexer` class
from __future__ import annotations

__all__ = [
    'CrupyParserBase',
]
from typing import Optional, IO, Any, NoReturn, TYPE_CHECKING, cast
from collections.abc import Callable

from crupydslparser.exception import CrupyDSLCoreException
from crupydslparser.parser._stream.stream import CrupyStream
from crupydslparser.parser.exception import CrupyParserBaseException
from crupydslparser.parser.node import CrupyParserNodeBase

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
    from crupydslparser.parser._lexer._operation.base import (
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
            list[Callable[[CrupyParserNodeBase], CrupyParserNodeBase]],
        ]= {}
        self._hook_error_book: dict[
            str,
            list[Callable[[CrupyParserBaseException], NoReturn]],
        ]= {}


    #---
    # Public properties
    #---

    @property
    def stream(self) -> CrupyStream:
        """ return the current stream if any """
        if self._stream:
            return self._stream
        raise CrupyDSLCoreException('No stream registered')

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
    ) -> CrupyParserNodeBase:
        """ execute a hook if available
        """
        hook_book = getattr(self, f"_hook_{target}_book")
        if production_name not in hook_book:
            if target == 'postprocess':
                return cast(CrupyParserNodeBase, args[0])
            raise args[0]
        try:
            node = None
            for hook in hook_book[production_name]:
                node = cast(CrupyParserNodeBase, hook(*args))
            if node is None:
                raise CrupyParserBaseException(
                    context = args[0].context,
                    reason  = \
                    f"{args[0].context.generate_error_log()}\n"
                    '\n'
                    f"Exception durring '{production_name}' hook, abort\n"
                    'Missing hooks'
                )
            return node
        except Exception as err:
            if target == 'error':
                raise err
            raise CrupyParserBaseException(
                context = args[0].context,
                reason  = \
                    f"{args[0].context.generate_error_log()}\n"
                    '\n'
                    f"Exception durring '{production_name}' hook, abort\n"
                    f"{err}"
            ) from err

    #---
    # Public methods
    #---

    def show(self, indent: int = 0) -> str:
        """ display production information
        """
        content = ''
        for production_info in self._production_book.items():
            if production_info[0] in self._hook_error_book:
                hook: Any = None
                for hook in self._hook_error_book[production_info[0]]:
                    hook = hook.__func__.__qualname__
                    content += f"{' ' * indent}@error({hook})\n"
            if production_info[0] in self._hook_postprocess_book:
                for hook in self._hook_postprocess_book[production_info[0]]:
                    hook = hook.__func__.__qualname__
                    content += f"{' ' * indent}@posthook({hook})\n"
            content += f"{' ' * indent}{production_info[0]}: \\\n"
            content += production_info[1].show(indent + 1)
            content += '\n'
            content += '\n'
        return content[:-2]

    def execute(self, production_name: str) -> CrupyParserNodeBase:
        """ execute a particular production name
        """
        if production_name not in self._production_book:
            raise CrupyDSLCoreException(
                'Unable to find the primary production entry name '
                f"'{production_name}'"
            )
        try:
            node = self._production_book[production_name](self)
            return self._execute_hook('postprocess', production_name, node)
        except CrupyParserBaseException as err:
            self._execute_hook('error', production_name, err)
            raise CrupyDSLCoreException(
                f"Error during {production_name} production handling"
            ) from err

    def register_stream(self, stream: CrupyStream|IO[str]|str) -> None:
        """ register a stream
        """
        if isinstance(stream, CrupyStream):
            self._stream = stream
        else:
            self._stream = CrupyStream.from_any(stream)

    def register_post_hook(
        self,
        production_name: str,
        hook: Callable[[CrupyParserNodeBase],CrupyParserNodeBase],
    ) -> None:
        """ register a new hook for a production
        """
        if production_name not in self._production_book:
            raise CrupyDSLCoreException(
                'Unable to find the primary production entry name '
                f"'{production_name}'"
            )
        if production_name not in self._hook_postprocess_book:
            self._hook_postprocess_book[production_name] = []
        self._hook_postprocess_book[production_name].append(hook)

    def register_error_hook(
        self,
        production_name: str,
        hook: Callable[[CrupyParserBaseException],NoReturn],
    ) -> None:
        """ register a new hook for a production in case of error
        """
        if production_name not in self._production_book:
            raise CrupyDSLCoreException(
                'Unable to find the primary production entry name '
                f"'{production_name}'"
            )
        if production_name not in self._hook_error_book:
            self._hook_error_book[production_name] = []
        self._hook_error_book[production_name].append(hook)
