"""
crupydslparser.parser.exception - parser exception class
"""
# use this magical import to allow partial class type reference
from __future__ import annotations

__all__ = [
    'CrupyParserBaseException',
]
from typing import Any, Optional

from crupydslparser.exception import CrupyDSLCoreException
from crupydslparser.parser._stream.context import CrupyStreamContext
from crupydslparser._utils import (
    crupynamedclass,
    crupyabstractclass,
)

#---
# Internals
#---

@crupyabstractclass
@crupynamedclass(
    generate_type   = True,
    regex           = '^Crupy(?P<type>([A-Z][a-z]+)+)Exception$',
)
class _CrupyParserAbstractException(CrupyDSLCoreException):
    """ Crupy parser exception class
    """
    def __init__(
        self,
        reason: str,
        context: CrupyStreamContext,
        *args: Any,
        message: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """ intialise the new object
        """
        if not message:
            message = reason
        super().__init__(message, *args, **kwargs)
        self._context = context
        self._reason  = reason
        self._message = message

    def __gt__(self, error: _CrupyParserAbstractException) -> bool:
        return self.context > error.context

    def __ge__(self, error: _CrupyParserAbstractException) -> bool:
        return self.context >= error.context

    def __getattr__(self, index: str) -> Any:
        """ workaround to trick pylint

        Since we use a lot of magic to generate this class, pylint is not
        able to understand what we do with all of the class decorator. So,
        we have a lot of "no-member" false-possitive, but if we provide this
        magic method, pylint do not throw the error.
        """

    #---
    # Properties
    #---

    @property
    def context(self) -> CrupyStreamContext:
        """ retrurn the stream context
        """
        return self._context

    @property
    def reason(self) -> str:
        """ return the reason of the exception
        """
        return self._reason

    @property
    def message(self) -> str:
        """ return the verbose exception message
        """
        return self._message

#---
# Public
#---

class CrupyParserBaseException(_CrupyParserAbstractException):
    """ crupy parser exception base class """
