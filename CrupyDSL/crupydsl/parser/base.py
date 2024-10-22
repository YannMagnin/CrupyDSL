"""
crupydsl.parser.base  - parser base class
"""
# @note
# Used as a workaround for the cyclic-import with the `CrupyDSLLexer` class
from __future__ import annotations

__all__ = [
    'CrupyDSLParserBase',
]
from typing import Optional, IO, Any, TYPE_CHECKING
from pathlib import Path
from collections.abc import Callable

from crupydsl.exception import CrupyDSLCoreException
from crupydsl.parser._stream.stream import CrupyDSLStream
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.parser.node import CrupyDSLParserNodeBase
from crupydsl._utils import (
    crupynamedclass,
    crupy_traceback_find,
)

# @note : Design mistake
#
# We cannot import the `CrupyDSLLexer` class since the magical `__call__()`
# method take a `CrupyDSLParserBase` class as a its first argument (which is
# defined here. So, we are in a circular dependencies problem.
#
# For now, I use a combination of workarounds to by-pass this bad design
# limitation:
# - use the `TYPE_CHECKING` indicator to know if we are in checking mode
# - use the `annotations` import to allow "not well defined class"
# - import the missing `CrupyDSLLexer` type
if TYPE_CHECKING:
    from crupydsl.parser._lexer._operation.op_base import (
        CrupyDSLLexerOpBase,
    )

#---
# Public
#---

@crupynamedclass(
    generate_type   = False,
    regex           = '^(_)*CrupyDSLParser(?P<type>([A-Z][a-z]+)+)$',
)
class CrupyDSLParserBase():
    """ Crupy parser class
    """
    def __init__(
        self,
        production_book: Optional[dict[str,CrupyDSLLexerOpBase]] = None,
    ) -> None:
        self._stream: CrupyDSLStream|None = None
        self._production_book: dict[str,CrupyDSLLexerOpBase] = {}
        if production_book:
            self._production_book = production_book
        self._hook_postprocess_book: dict[
            str,
            list[
                Callable[
                    [CrupyDSLParserNodeBase],
                    CrupyDSLParserNodeBase,
                ],
            ],
        ]= {}
        self._hook_error_book: dict[
            str,
            list[
                Callable[
                    [CrupyDSLParserBaseException],
                    CrupyDSLParserBaseException
                ],
            ],
        ]= {}


    #---
    # Public properties
    #---

    @property
    def stream(self) -> CrupyDSLStream:
        """ return the current stream if any """
        if self._stream:
            return self._stream
        raise CrupyDSLCoreException('No stream registered')

    @property
    def production_book(self) -> dict[str,CrupyDSLLexerOpBase]:
        """ return the current registered rules """
        return self._production_book

    #---
    # Internal methods
    #---

    def _execute_hook_postprocess(
        self,
        production_name: str,
        node: CrupyDSLParserNodeBase,
    ) -> CrupyDSLParserNodeBase:
        """ execute a postprocess hook if available
        """
        if production_name not in self._hook_postprocess_book:
            return node
        for hook in self._hook_postprocess_book[production_name]:
            node = hook(node)
        return node

    def _execute_hook_error(
        self,
        production_name: str,
        error: CrupyDSLParserBaseException,
    ) -> CrupyDSLParserBaseException:
        """ execute all error hook for the current production
        """
        if production_name not in self._hook_error_book:
            return error
        for hook in self._hook_error_book[production_name]:
            error = hook(error)
        return error

    #---
    # Public methods
    #---

    def execute(self, production_name: str) -> CrupyDSLParserNodeBase:
        """ execute a particular production name
        """
        if production_name not in self._production_book:
            raise CrupyDSLCoreException(
                'Unable to find the primary production entry name '
                f"'{production_name}'"
            )
        try:
            node = self._production_book[production_name](self)
            return self._execute_hook_postprocess(production_name, node)
        except CrupyDSLParserBaseException as err:
            try:
                error = self._execute_hook_error(production_name, err)
            except Exception as err2:
                raise CrupyDSLCoreException(
                    f"Exception durring '{production_name}' hook, abort\n"
                    f"{err2}\n"
                    f"{crupy_traceback_find()}"
                ) from err2
        raise error

    def register_stream(
        self,
        stream: Path|IO[str]|str|CrupyDSLStream,
    ) -> None:
        """ register a stream
        """
        self._stream = CrupyDSLStream.from_any(stream)

    def register_post_hook(
        self,
        production_name: str,
        hook: Callable[
            [CrupyDSLParserNodeBase],
            CrupyDSLParserNodeBase,
        ],
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
        hook: Callable[
            [CrupyDSLParserBaseException],
            CrupyDSLParserBaseException,
        ],
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

    def debug_show(self, indent: int = 0) -> str:
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
                for hook in self._hook_postprocess_book[
                    production_info[0]
                ]:
                    hook = hook.__func__.__qualname__
                    content += f"{' ' * indent}@posthook({hook})\n"
            content += f"{' ' * indent}{production_info[0]}: \\\n"
            content += production_info[1].debug_show(indent + 1)
            content += '\n'
            content += '\n'
        return content[:-2]
