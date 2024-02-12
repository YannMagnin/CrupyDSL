"""
crupydslparser.core._lexer.op_until - Lexer read until operation
"""
__all__ = [
    'CrupyLexerTokenUntil',
    'CrupyLexerUntil',
]

from crupydslparser.core._lexer._lexer import CrupyLexer
from crupydslparser.core._lexer._token import CrupyLexerToken
from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyLexerTokenUntil(CrupyLexerToken):
    """ string token information """
    text: str

class CrupyLexerUntil(CrupyLexer):
    """ strict string matcher
    """
    def __init__(self, delimiter: str) -> None:
        self._delimiter = delimiter

    def __call__(self, stream: CrupyStream) -> CrupyLexerToken|None:
        """ try to strictly match the text
        """
        with stream as lexem:
            if lexem.read_char() != self._delimiter:
                return None
            content = ''
            while True:
                if not (curr := lexem.read_char()):
                    return None
                if curr == self._delimiter:
                    break
                content += curr
            return CrupyLexerTokenUntil(
                stream_ctx  = lexem.validate(),
                text        = content,
            )
