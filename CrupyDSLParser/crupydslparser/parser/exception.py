"""
crupydslparser.parser.exception - parser exception class
"""
__all__ = [
    'CrupyParserBaseException',
]
from typing import Optional

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
        message: Optional[str] = None,
        context: Optional[CrupyStreamContext] = None,
    ) -> None:
        """ intialise the new object
        """
        if message is None:
            message = reason
        if context:
            message = f"{context.generate_error_log()}\n{message}"
        super().__init__(message)
        self._context = context
        self._reason  = reason
        self._message = reason

    #---
    # Properties
    #---

    @property
    def context(self) -> CrupyStreamContext:
        """ retrurn the stream context
        """
        if self._context is not None:
            return self._context
        raise self.__class__(
            'Accessing stream non existing stream context in lexer '
            'exception'
        )

    @property
    def reason(self) -> str:
        """ return the reason of the exception
        """
        return self._reason

#---
# Public
#---

class CrupyParserBaseException(_CrupyParserAbstractException):
    """ crupy parser exception base class """
