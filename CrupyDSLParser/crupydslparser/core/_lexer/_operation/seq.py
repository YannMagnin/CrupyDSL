"""
crupydslparser.core._lexer._operation.seq   - sequence operation
"""
__all__ = [
    'CrupyParserNodeLexSeq',
    'CrupyLexerOpSeq',
]
from typing import List, Any, cast

from crupydslparser.core._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.core._lexer._assert._base import CrupyLexerAssertBase
from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Public
#---

class CrupyParserNodeLexSeq(CrupyParserNode):
    """ sequence token information """
    seq: List[CrupyParserNode]


# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238
class CrupyLexerOpSeq(CrupyLexerOpBase):
    """ execute sequence of lexer operation
    """
    def __init__(self, *args: Any) -> None:
        self._seq: List[CrupyLexerOpBase|CrupyLexerAssertBase] = []
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

    def _execute(
        self,
        parser: CrupyParserBase,
        last_chance: bool,
    ) -> CrupyParserNode|None:
        """ execute all lexer operation
        """
        with parser.stream as lexem:
            token_list: List[CrupyParserNode] = []
            for lexer in self._seq:
                last_chance_really = False
                if lexer == self._seq[-1]:
                    last_chance_really = last_chance
                if issubclass(type(lexer), CrupyLexerAssertBase):
                    assert_op = cast(CrupyLexerAssertBase, lexer)
                    if not assert_op(parser):
                        return None
                else:
                    lexer_op = cast(CrupyLexerOpBase, lexer)
                    if not (token := lexer_op(parser, last_chance_really)):
                        return None
                    token_list.append(token)
            return CrupyParserNodeLexSeq(
                stream_ctx  = lexem.validate(),
                seq         = token_list
            )
