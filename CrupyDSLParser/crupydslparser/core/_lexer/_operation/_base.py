"""
crupydslparser.core._lexer._operation._base - Lexer operation abstraction
"""
__all__ = [
    'CrupyLexerOpBase',
]
from typing import Dict, Any
from abc import ABC, abstractmethod

from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Public
#---

# allow too few public methods
# pylint: disable=locally-disabled,R0903
class CrupyLexerOpBase(ABC):
    """ Lexer capture operation
    """

    #---
    # Magic mechanism used to ensure class formalism
    #---

    def __init_subclass__(cls, /, **kwargs: Dict[str,Any]) -> None:
        """ guess token name based on class name
        """
        if (
                cls.__name__.find('CrupyLexerOp') != 0
            and cls.__name__.find('_CrupyLexerOp') != 0
        ):
            raise CrupyLexerException(
                f"Malformated lexer operation class name '{cls.__name__}'"
            )

    #---
    # Magic operation and error handling
    #---

    def __call__(
        self,
        parser: CrupyParserBase,
        last_chance: bool,
    ) -> CrupyParserNode|None:
        """ lexer operation trampoline (used to handle error if needed)
        """
        if type(self).__call__ != CrupyLexerOpBase.__call__:
            raise CrupyLexerException(
                'The magical method `CrupyLexerOpBase` as been overridden '
                f"in class `{type(self).__name__}` which is forbidden"
            )
        if not hasattr(self, '_execute'):
            raise CrupyLexerException(
                f"The class {type(self).__name__} do not "
                'expose the `_execute` methods'
            )
        node = self._execute(parser, last_chance)
        if last_chance and not node:
            raise CrupyLexerException.from_operation(parser)
        return node

    @abstractmethod
    def _execute(
        self,
        parser: CrupyParserBase,
        last_chance: bool,
    ) -> CrupyParserNode|None:
        """ internal core operation code """
