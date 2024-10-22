"""
crupydsl.parser._lexer._operation.seq - sequence operation
"""
__all__ = [
    'CrupyDSLLexerOpSeq',
    'CrupyDSLLexerOpSeqException',
    'CrupyDSLParserNodeLexSeq',
]
from typing import Union, Any, cast

from crupydsl.parser._lexer._operation.op_base import CrupyDSLLexerOpBase
from crupydsl.parser._lexer._assert.base import CrupyDSLLexerAssertBase
from crupydsl.parser._lexer.exception import CrupyDSLLexerException
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser.node import CrupyDSLParserNodeBase
from crupydsl.exception import CrupyDSLCoreException

#---
# Public
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

class CrupyDSLParserNodeLexSeq(CrupyDSLParserNodeBase):
    """ sequence token information """
    seq: list[CrupyDSLParserNodeBase]

class CrupyDSLLexerOpSeqException(CrupyDSLLexerException):
    """ class exception for seq operation """
    validated_operation: int

class CrupyDSLLexerOpSeq(CrupyDSLLexerOpBase):
    """ execute sequence of lexer operation
    """
    def __init__(self, *args: Any) -> None:
        super().__init__()
        self._seq: list[
            Union[CrupyDSLLexerOpBase,CrupyDSLLexerAssertBase]
        ] = []
        for i, arg in enumerate(args):
            if (
                    CrupyDSLLexerOpBase not in type(arg).mro()
                and CrupyDSLLexerAssertBase not in type(arg).mro()
            ):
                raise CrupyDSLCoreException(
                    f"Unable to initialise the {type(self).__name__} "
                    f"because the argument {i} is not of type CrupyDSLLexer "
                    f"({type(arg).mro()})"
                )
            self._seq.append(arg)
        if not self._seq:
            raise CrupyDSLCoreException(
                f"Unable to initialise the {type(self).__name__} because "
                'not sequence has been presented'
            )

    def __call__(self, parser: CrupyDSLParserBase) -> CrupyDSLParserNodeBase:
        """ execute all lexer operation
        """
        with parser.stream as context:
            token_list: list[CrupyDSLParserNodeBase] = []
            for i, lexer in enumerate(self._seq):
                try:
                    if issubclass(type(lexer), CrupyDSLLexerAssertBase):
                        assert_op = cast(CrupyDSLLexerAssertBase, lexer)
                        if not assert_op(parser):
                            raise CrupyDSLLexerOpSeqException(
                                context             = context,
                                validated_operation = i,
                                reason              = \
                                    'unable to validate the assertion '
                                    f"{assert_op.type}"
                            )
                        continue
                    token_list.append(
                        cast(CrupyDSLLexerOpBase, lexer)(parser)
                    )
                except CrupyDSLParserBaseException as err:
                    context.index = err.context.index
                    context.lineno = err.context.lineno
                    context.column = err.context.column
                    raise CrupyDSLLexerOpSeqException(
                        context             = context,
                        validated_operation = i,
                        reason              = err.reason,
                        message             = err.message,
                    ) from err
            return CrupyDSLParserNodeLexSeq(
                context = context.validate(),
                seq     = token_list,
            )

    #---
    # Public methods
    #---

    def debug_show(self, indent: int = 0) -> str:
        """ display a generic information
        """
        content = f"{' ' * indent}{type(self).__name__}(\n"
        for alternative in self._seq:
            content += alternative.debug_show(indent + 1)
            content += ',\n'
        content += f"{' ' * indent})"
        return content
