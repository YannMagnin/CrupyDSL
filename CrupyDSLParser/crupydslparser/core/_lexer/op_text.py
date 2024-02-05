"""
crupydslparser.core._lexer.op_text  - Lexer text tool
"""
__all__ = [
    'CrupyLexerTokenText',
    'CrupyLexerText',
]

from crupydslparser.core._lexer._lexer import CrupyLexer
from crupydslparser.core._lexer._token import CrupyLexerToken
from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyLexerTokenText(CrupyLexerToken):
    """ string token information """
    text: str

class CrupyLexerText(CrupyLexer):
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
            return CrupyLexerTokenText(
                stream_ctx  = lexem.validate(),
                text        = self._text,
            )
