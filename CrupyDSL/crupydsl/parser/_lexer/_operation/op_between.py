
"""
crupydsl.parser._lexer._operation.between - between operation
"""
__all__ = [
    'CrupyDSLLexerOpBetween',
    'CrupyDSLLexerOpBetweenException',
    'CrupyDSLParserNodeLexBetween',
]
from typing import Union

from crupydsl.parser._lexer._operation.op_base import CrupyDSLLexerOpBase
from crupydsl.parser._lexer._assert.base import CrupyDSLLexerAssertBase
from crupydsl.parser._lexer.exception import CrupyDSLLexerException
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.parser.node import CrupyDSLParserNodeBase
from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser._lexer._operation.op_builtin import (
    CrupyDSLLexerOpBuiltin,
)
#---
# Public
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

class CrupyDSLParserNodeLexBetween(CrupyDSLParserNodeBase):
    """ between token information """
    captured_start:     CrupyDSLParserNodeBase
    captured_middle:    str
    captured_end:       CrupyDSLParserNodeBase

class CrupyDSLLexerOpBetweenException(CrupyDSLLexerException):
    """ class exception for seq operation """
    validated_operation: int
    original_reason: str

class CrupyDSLLexerOpBetween(CrupyDSLLexerOpBase):
    """ execute sequence of lexer operation
    """
    def __init__(
        self,
        startop: Union[CrupyDSLLexerOpBase, CrupyDSLLexerAssertBase],
        endop: Union[CrupyDSLLexerOpBase, CrupyDSLLexerAssertBase],
        with_newline: bool,
    ) -> None:
        super().__init__()
        self._startop = startop
        self._endop = endop
        self._with_newline = with_newline

    def __call__(
        self,
        parser: CrupyDSLParserBase,
    ) -> CrupyDSLParserNodeBase:
        """ execute all lexer operation
        """
        if self._with_newline:
            anyop = CrupyDSLLexerOpBuiltin('any_newline')
        else:
            anyop = CrupyDSLLexerOpBuiltin('any')
        validated_operation = 0
        with parser.stream as context:
            try:
                captured_start = self._startop(parser)
                if (
                        isinstance(self._startop, CrupyDSLLexerAssertBase)
                    and captured_start is False
                ):
                    raise CrupyDSLParserBaseException(
                        reason  = 'invalid input stream',
                        context = context,
                    )
                validated_operation = 1
                captured_middle = ''
                while True:
                    try:
                        captured_end = self._endop(parser)
                        if not isinstance(
                            self._endop,
                            CrupyDSLLexerAssertBase,
                        ):
                            validated_operation = 2
                            break
                        if captured_end:
                            validated_operation = 2
                            break
                    except CrupyDSLParserBaseException as err:
                        if err.reason == 'reached end-of-file':
                            validated_operation = 2
                            raise err
                    captured_middle += anyop(parser).text
            except CrupyDSLParserBaseException as err:
                context.index = err.context.index
                context.lineno = err.context.lineno
                context.column = err.context.column
                if validated_operation == 0:
                    reason = 'unable to validate the opening request: '
                elif validated_operation == 1:
                    reason = 'unable to validate the middle request: '
                else:
                    reason = 'unable to validate the enclosing request: '
                raise CrupyDSLLexerOpBetweenException(
                    context             = context,
                    validated_operation = validated_operation,
                    original_reason     = err.reason,
                    reason              = f"{reason}{err.reason}",
                ) from err
            return CrupyDSLParserNodeLexBetween(
                context         = context.validate(),
                captured_start  = captured_start,
                captured_middle = captured_middle,
                captured_end    = captured_end,
            )

    #---
    # Public methods
    #---

    def show(self, indent: int = 0) -> str:
        """ display a generic information
        """
        content  = ' ' * indent
        content += self._startop.show()
        content += '.!.' if self._with_newline else '...'
        content += self._endop.show()
        return content
