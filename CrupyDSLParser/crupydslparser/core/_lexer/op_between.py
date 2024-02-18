"""
crupydslparser.core._lexer.op_between   - Lexer between delimiter operation
"""
__all__ = [
    'CrupyParserNodeLexBetween',
    'CrupyLexerBetween',
]

from crupydslparser.core._lexer._lexer import CrupyLexer
from crupydslparser.core.parser._base import CrupyParserBase
from crupydslparser.core.parser.node import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeLexBetween(CrupyParserNode):
    """ string node information """
    text: str

class CrupyLexerBetween(CrupyLexer):
    """ capture between delimiter
    """
    def __init__(self, delimiter: str) -> None:
        self._delimiter = delimiter

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode|None:
        """ try to strictly match the text
        """
        with parser.stream as lexem:
            if lexem.read_char() != self._delimiter:
                return None
            content = ''
            while True:
                if not (curr := lexem.read_char()):
                    return None
                if curr == self._delimiter:
                    break
                content += curr
            return CrupyParserNodeLexBetween(
                stream_ctx  = lexem.validate(),
                text        = content,
            )