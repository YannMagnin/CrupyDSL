"""
crupydsl.parser.exception - parser exception class
"""
# use this magical import to allow partial class type reference
from __future__ import annotations

__all__ = [
    'CrupyDSLParserBaseException',
]
from typing import Any, Optional

from crupydsl.exception import CrupyDSLCoreException
from crupydsl.parser._stream.context import CrupyDSLStreamContext
from crupydsl._utils import (
    crupynamedclass,
    crupyabstractclass,
)

#---
# Internals
#---

@crupyabstractclass
@crupynamedclass(
    generate_type   = True,
    regex           = '^CrupyDSL(?P<type>([A-Z][a-z]+)+)Exception$',
)
class _CrupyDSLParserAbstractException(CrupyDSLCoreException):
    """ Crupy parser exception class
    """
    def __init__(
        self,
        reason: str,
        context: CrupyDSLStreamContext,
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

    def __gt__(self, error: _CrupyDSLParserAbstractException) -> bool:
        return self.context > error.context

    def __ge__(self, error: _CrupyDSLParserAbstractException) -> bool:
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
    def context(self) -> CrupyDSLStreamContext:
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

class CrupyDSLParserBaseException(_CrupyDSLParserAbstractException):
    """ crupy parser exception base class """
