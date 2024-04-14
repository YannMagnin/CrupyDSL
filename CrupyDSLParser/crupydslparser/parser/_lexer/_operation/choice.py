"""
crupydslparser.parser._lexer._operation.choice    - lexer or operation
"""
__all__ = [
    'CrupyLexerOpOr',
    'CrupyLexerOpOrException',
]
from typing import Any

from crupydslparser.parser._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.parser._lexer.exception import CrupyLexerException
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

class CrupyLexerOpOrException(CrupyLexerException):
    """ exception class """
    deepest_error: CrupyLexerException

class CrupyLexerOpOr(CrupyLexerOpBase):
    """ OR lexer operation
    """
    def __init__(self, *args: Any) -> None:
        self._seq: list[CrupyLexerOpBase] = []
        for i, arg in enumerate(args):
            if CrupyLexerOpBase not in type(arg).mro():
                raise CrupyParserBaseException(
                    f"Unable to initialise the {type(arg).__name__} "
                    f"because the argument {i} is not of type "
                    f"CrupyLexerOpBase ({type(arg).__name__})"
                )
            self._seq.append(arg)
        if not self._seq:
            raise CrupyParserBaseException(
                f"Unable to initialise the {self.__class__.__name__} "
                "because not sequence has been presented"
            )

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ try to match at least one of the two lexer operation
        """
        best_choice_error: CrupyLexerException|None = None
        for lexer in self._seq:
            try:
                return lexer(parser)
            except CrupyLexerException as err:
                if best_choice_error is None:
                    best_choice_error = err
                    continue
                if best_choice_error.context < err.context:
                    best_choice_error = err
        if not best_choice_error:
            with parser.stream as context:
                raise CrupyLexerOpOrException(
                    context         = context,
                    deepest_error   = None,
                    reason          = \
                        'unable to validate the sequense, empty sequense',
                )
        raise CrupyLexerOpOrException(
            context         = best_choice_error.context,
            deepest_error   = best_choice_error.context,
            reason          = \
                'unable to find an alternative that match the provided '
                f"stream. Reason: {best_choice_error.reason}",
        )
