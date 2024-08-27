"""
crupydslparser.parser._lexer._operation.choice    - lexer or operation
"""
__all__ = [
    'CrupyLexerOpOr',
    'CrupyLexerOpOrException',
]
from typing import Union, Any

from crupydslparser.parser._lexer._operation.base import CrupyLexerOpBase
from crupydslparser.parser._lexer.exception import CrupyLexerException
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser.parser.exception import CrupyParserBaseException
from crupydslparser.exception import CrupyDSLCoreException

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
        super().__init__()
        self._seq: list[CrupyLexerOpBase] = []
        for i, arg in enumerate(args):
            if CrupyLexerOpBase not in type(arg).mro():
                raise CrupyDSLCoreException(
                    f"Unable to initialise the {type(arg).__name__} "
                    f"because the argument {i} is not of type "
                    f"CrupyLexerOpBase ({type(arg).__name__})"
                )
            self._seq.append(arg)
        if not self._seq:
            raise CrupyDSLCoreException(
                f"Unable to initialise the {self.__class__.__name__} "
                "because not sequence has been presented"
            )

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ try to match at least one of the two lexer operation
        """
        best_choice_error_special = False
        best_choice_error: Union[CrupyParserBaseException,None] = None
        for lexer in self._seq:
            try:
                return lexer(parser)
            except CrupyParserBaseException as err:
                if type(err).__name__ == 'CrupyLexerErrorException':
                    if best_choice_error and best_choice_error_special:
                        best_choice_error = max(best_choice_error, err)
                    else:
                        best_choice_error = err
                    best_choice_error_special = True
                elif best_choice_error is None:
                    best_choice_error = err
                else:
                    best_choice_error = max(best_choice_error, err)
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
            deepest_error   = best_choice_error,
            reason          = best_choice_error.reason,
            message         = best_choice_error.message,
        )

    #---
    # Public methods
    #---

    def show(self, indent: int = 0) -> str:
        """ display a generic information
        """
        content = f"{' ' * indent}{type(self).__name__}(\n"
        for alternative in self._seq:
            content += alternative.show(indent + 1)
            content += ',\n'
        content += f"{' ' * indent})"
        return content
