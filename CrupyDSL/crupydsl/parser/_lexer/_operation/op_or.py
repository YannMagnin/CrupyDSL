"""
crupydsl.parser._lexer._operation.choice    - lexer or operation
"""
__all__ = [
    'CrupyDSLLexerOpOr',
    'CrupyDSLLexerOpOrException',
]
from typing import Union, Any

from crupydsl.parser._lexer._operation.op_base import CrupyDSLLexerOpBase
from crupydsl.parser._lexer.exception import CrupyDSLLexerException
from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser.node import CrupyDSLParserNodeBase
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.exception import CrupyDSLCoreException

#---
# Public
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

class CrupyDSLLexerOpOrException(CrupyDSLLexerException):
    """ exception class """
    deepest_error: CrupyDSLLexerException

class CrupyDSLLexerOpOr(CrupyDSLLexerOpBase):
    """ OR lexer operation
    """
    def __init__(self, *args: Any) -> None:
        super().__init__()
        self._seq: list[CrupyDSLLexerOpBase] = []
        for i, arg in enumerate(args):
            if CrupyDSLLexerOpBase not in type(arg).mro():
                raise CrupyDSLCoreException(
                    f"Unable to initialise the {type(arg).__name__} "
                    f"because the argument {i} is not of type "
                    f"CrupyDSLLexerOpBase ({type(arg).__name__})"
                )
            self._seq.append(arg)
        if not self._seq:
            raise CrupyDSLCoreException(
                f"Unable to initialise the {self.__class__.__name__} "
                "because not sequence has been presented"
            )

    def __call__(self, parser: CrupyDSLParserBase) -> CrupyDSLParserNodeBase:
        """ try to match at least one of the two lexer operation
        """
        best_choice_error_special = False
        best_choice_error: Union[CrupyDSLParserBaseException,None] = None
        for lexer in self._seq:
            try:
                return lexer(parser)
            except CrupyDSLParserBaseException as err:
                if type(err).__name__ == 'CrupyDSLLexerErrorException':
                    if best_choice_error and best_choice_error_special:
                        best_choice_error = max(best_choice_error, err)
                    else:
                        best_choice_error = err
                    best_choice_error_special = True
                elif best_choice_error is None:
                    best_choice_error = err
                elif best_choice_error <= err:
                    best_choice_error = err
        if not best_choice_error:
            with parser.stream as context:
                raise CrupyDSLLexerOpOrException(
                    context         = context,
                    deepest_error   = None,
                    reason          = \
                        'unable to validate the sequense, empty sequense',
                )
        raise CrupyDSLLexerOpOrException(
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
