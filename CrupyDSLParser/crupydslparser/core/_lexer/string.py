"""
crupydslparser.core._lexer.string    - Lexer string tool
"""
__all__ = [
    'CrupyLexerString',
]

from crupydslparser.core._lexer._lexer import CrupyLexer
from crupydslparser.core._lexer._token import CrupyLexerToken
from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyLexerTokenString(CrupyLexerToken):
    """ string token information """
    text: str

class CrupyLexerString(CrupyLexer):
    """ strict string matcher
    """
    def __init__(self, text: str) -> None:
        self._text = text

    def __call__(self, stream: CrupyStream) -> CrupyLexerToken|None:
        """ try to strictly match the text
        """
        with stream as stream_ctx:
            if stream.peek_string(self._text):
                return CrupyLexerTokenString(
                    stream_ctx  = stream_ctx.validate(),
                    text        = self._text,
                )
        return None
