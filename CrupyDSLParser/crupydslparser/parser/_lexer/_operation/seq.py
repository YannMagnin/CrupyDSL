"""
crupydslparser.parser._lexer._operation.seq - sequence operation
"""
__all__ = [
    'CrupyLexerOpSeq',
]
from typing import Any, cast

from crupydslparser.parser._lexer._operation.base import CrupyLexerOpBase
from crupydslparser.parser._lexer._assert.base import CrupyLexerAssertBase
from crupydslparser.parser._lexer.exception import CrupyLexerException
from crupydslparser.parser.exception import CrupyParserBaseException
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser.exception import CrupyDSLCoreException

#---
# Public
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

class CrupyParserNodeLexSeq(CrupyParserNodeBase):
    """ sequence token information """
    seq: list[CrupyParserNodeBase]

class CrupyLexerOpSeqException(CrupyLexerException):
    """ class exception for seq operation """
    validated_operation: int

class CrupyLexerOpSeq(CrupyLexerOpBase):
    """ execute sequence of lexer operation
    """
    def __init__(self, *args: Any) -> None:
        super().__init__()
        self._seq: list[CrupyLexerOpBase|CrupyLexerAssertBase] = []
        for i, arg in enumerate(args):
            if (
                    CrupyLexerOpBase not in type(arg).mro()
                and CrupyLexerAssertBase not in type(arg).mro()
            ):
                raise CrupyDSLCoreException(
                    f"Unable to initialise the {type(self).__name__} "
                    f"because the argument {i} is not of type CrupyLexer "
                    f"({type(arg).mro()})"
                )
            self._seq.append(arg)
        if not self._seq:
            raise CrupyDSLCoreException(
                f"Unable to initialise the {type(self).__name__} because "
                'not sequence has been presented'
            )

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ execute all lexer operation
        """
        with parser.stream as context:
            token_list: list[CrupyParserNodeBase] = []
            for i, lexer in enumerate(self._seq):
                try:
                    if issubclass(type(lexer), CrupyLexerAssertBase):
                        assert_op = cast(CrupyLexerAssertBase, lexer)
                        if not assert_op(parser):
                            raise CrupyLexerOpSeqException(
                                context             = context,
                                validated_operation = i,
                                reason              = \
                                    'unable to validate the assertion '
                                    f"{assert_op.type}"
                            )
                        continue
                    token_list.append(
                        cast(CrupyLexerOpBase, lexer)(parser)
                    )
                except CrupyParserBaseException as err:
                    context.index = err.context.index
                    context.lineno = err.context.lineno
                    context.column = err.context.column
                    raise CrupyLexerOpSeqException(
                        context             = context,
                        validated_operation = i,
                        reason              = err.reason,
                        message             = err.message,
                    ) from err
            return CrupyParserNodeLexSeq(
                context = context.validate(),
                seq     = token_list,
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
