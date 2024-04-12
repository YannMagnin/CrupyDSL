"""
crupydslparser.parser._lexer._operation.seq - sequence operation
"""
__all__ = [
    'CrupyParserNodeLexSeq',
    'CrupyLexerOpSeq',
]
from typing import Any, cast

from crupydslparser.parser._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.parser._lexer._assert._base import CrupyLexerAssertBase
from crupydslparser.parser._lexer.exception import CrupyLexerException
from crupydslparser.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Public
#---

class CrupyParserNodeLexSeq(CrupyParserNode):
    """ sequence token information """
    seq: list[CrupyParserNode]


# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238
class CrupyLexerOpSeq(CrupyLexerOpBase):
    """ execute sequence of lexer operation
    """
    def __init__(self, *args: Any) -> None:
        self._seq: list[CrupyLexerOpBase|CrupyLexerAssertBase] = []
        for i, arg in enumerate(args):
            if (
                    CrupyLexerOpBase not in type(arg).mro()
                and CrupyLexerAssertBase not in type(arg).mro()
            ):
                raise CrupyLexerException(
                    f"Unable to initialise the {type(self).__name__} "
                    f"because the argument {i} is not of type CrupyLexer "
                    f"({type(arg).mro()})"
                )
            self._seq.append(arg)
        if not self._seq:
            raise CrupyLexerException(
                f"Unable to initialise the {type(self).__name__} because "
                'not sequence has been presented'
            )

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode:
        """ execute all lexer operation
        """
        with parser.stream as context:
            token_list: list[CrupyParserNode] = []
            for i, lexer in enumerate(self._seq):
                try:
                    if issubclass(type(lexer), CrupyLexerAssertBase):
                        assert_op = cast(CrupyLexerAssertBase, lexer)
                        if not assert_op(parser):
                            self._raise_from_context(
                                context,
                                'Unable to validate the assertion '
                                f"{assert_op.name}"
                            )
                        continue
                    token_list.append(
                        cast(CrupyLexerOpBase, lexer)(parser)
                    )
                except CrupyLexerException as err:
                    context.index = err.context.index
                    context.lineno = err.context.lineno
                    context.column = err.context.column
                    self._raise_from_context(
                        context,
                        f"Unable to validate the operation number {i + 1}",
                    )
            return CrupyParserNodeLexSeq(
                context = context.validate(),
                seq     = token_list,
            )
