"""
crupydslparser.core._lexer._operation.seq   - sequence operation
"""
__all__ = [
    'CrupyParserNodeLexSeq',
    'CrupyLexerOpSeq',
]
from typing import List, Any

from crupydslparser.core._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core.parser._base import CrupyParserBase
from crupydslparser.core.parser.node import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeLexSeq(CrupyParserNode):
    """ sequence token information """
    seq: List[CrupyParserNode]

class CrupyLexerOpSeq(CrupyLexerOpBase):
    """ execute sequence of lexer operation
    """
    def __init__(self, *args: Any) -> None:
        self._seq: List[CrupyLexerOpBase] = []
        for i, arg in enumerate(args):
            if CrupyLexerOpBase not in type(arg).mro():
                raise CrupyLexerException(
                    'Unable to initialise the CrupyLexerSeq because the '
                    f"argument {i} is not of type CrupyLexer "
                    f"({type(arg)})"
                )
            self._seq.append(arg)
        if not self._seq:
            raise CrupyLexerException(
                'Unable to initialise the CrupyLexerSeq because not '
                'sequence has been presented'
            )

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode|None:
        """ execute all lexer operation
        """
        with parser.stream as lexem:
            token_list: List[CrupyParserNode] = []
            for lexer in self._seq:
                if not (token := lexer(parser)):
                    return None
                token_list.append(token)
            return CrupyParserNodeLexSeq(
                stream_ctx  = lexem.validate(),
                seq         = token_list
            )
