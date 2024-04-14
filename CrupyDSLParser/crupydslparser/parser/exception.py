"""
crupydslparser.parser.exception - parser exception class
"""
__all__ = [
    'CrupyParserBaseException',
]
from typing import Optional, Any
import re

from crupydslparser.exception import CrupyDSLCoreException
from crupydslparser.parser._stream.context import CrupyStreamContext

#---
# Internals
#---

class _CrupyParserAbstractException(CrupyDSLCoreException):
    """ Crupy parser exception class """
    _type: str

    #---
    # Magic class
    #---

    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        """ check the subclass name validity
        """
        if not (
            info := re.match(
                '^CrupyParser(?P<name>([A-Z][a-z]+)+)Exception$',
                cls.__name__,
            )
        ):
            raise CrupyDSLCoreException(
                f"Subclass '{cls.__name__}' is malformated"
            )
        cls._type = ''
        for letter in info['name']:
            if cls._type and letter.isupper():
                cls._type += '_'
            cls._type += letter.lower()

    #---
    # Magic object
    #---

    def __init__(
        self,
        message: str,
        context: Optional[CrupyStreamContext] = None,
    ) -> None:
        """ intialise the new object
        """
        reason = message
        if context:
            message = f"{context.generate_error_log()}\n{message}"
        super().__init__(message)
        self._context = context
        self._reason = reason

    def __getattr__(self, name: str) -> Any:
        """ return the attribute `name`

        @note
        We are constraint to raise `AttributeError` if the attribute `name`
        is not found, otherwise the `getattr(obj, key, default)` will never
        return the default value
        """
        if name in self.__dict__:
            return self.__dict__[name]
        if name in self.__class__.__dict__:
            return self.__class__.__dict__[name]
        raise AttributeError(
            f"Unable to fetch the attribute '{name}' for the class "
            f"{self.__class__.__name__}"
        )

    #---
    # Properties
    #---

    @property
    def type(self) -> str:
        """ return the class type """
        return self._type

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
