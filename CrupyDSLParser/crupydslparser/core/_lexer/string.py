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
        with stream as lexem:
            for char in self._text:
                if lexem.read_char() != char:
                    return None
            return CrupyLexerTokenString(
                stream_ctx  = lexem.validate(),
                text        = self._text,
            )
