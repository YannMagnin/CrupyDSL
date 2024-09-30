
"""
crupydslparser.parser._lexer._operation.between - between operation
"""
__all__ = [
    'CrupyLexerOpBetween',
    'CrupyLexerOpBetweenException',
    'CrupyParserNodeLexBetween',
]

from crupydslparser.parser._lexer._operation.op_base import CrupyLexerOpBase
from crupydslparser.parser._lexer.exception import CrupyLexerException
from crupydslparser.parser.exception import CrupyParserBaseException
from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser._lexer._operation.op_builtin import (
    CrupyLexerOpBuiltin,
)
#---
# Public
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

class CrupyParserNodeLexBetween(CrupyParserNodeBase):
    """ between token information """
    captured_start:     CrupyParserNodeBase
    captured_middle:    str
    captured_end:       CrupyParserNodeBase

class CrupyLexerOpBetweenException(CrupyLexerException):
    """ class exception for seq operation """
    validated_operation: int
    original_reason: str

class CrupyLexerOpBetween(CrupyLexerOpBase):
    """ execute sequence of lexer operation
    """
    def __init__(
        self,
        startop: CrupyLexerOpBase,
        endop: CrupyLexerOpBase,
        with_newline: bool,
    ) -> None:
        super().__init__()
        self._startop = startop
        self._endop = endop
        self._with_newline = with_newline

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ execute all lexer operation
        """
        if self._with_newline:
            anyop = CrupyLexerOpBuiltin('any_newline')
        else:
            anyop = CrupyLexerOpBuiltin('any')
        validated_operation = 0
        with parser.stream as context:
            try:
                captured_start = self._startop(parser)
                validated_operation = 1
                captured_middle = ''
                while True:
                    try:
                        captured_end = self._endop(parser)
                        validated_operation = 2
                        break
                    except CrupyParserBaseException as err:
                        if err.reason == 'reached end-of-file':
                            validated_operation = 2
                            raise err
                    captured_middle += anyop(parser).text
            except CrupyParserBaseException as err:
                context.index = err.context.index
                context.lineno = err.context.lineno
                context.column = err.context.column
                if validated_operation == 0:
                    reason = 'unable to validate the opening request: '
                elif validated_operation == 1:
                    reason = 'unable to validate the middle request: '
                else:
                    reason = 'unable to validate the enclosing request: '
                raise CrupyLexerOpBetweenException(
                    context             = context,
                    validated_operation = validated_operation,
                    original_reason     = err.reason,
                    reason              = f"{reason}{err.reason}",
                ) from err
            return CrupyParserNodeLexBetween(
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
