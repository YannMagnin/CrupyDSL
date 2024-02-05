"""
crupydslparser.core._lexer.op_seq   - sequence operation
"""
__all__ = [
    'CrupyLexerTokenSeq',
    'CrupyLexerSeq',
]
from typing import List, Any

from crupydslparser.core._lexer._lexer import CrupyLexer
from crupydslparser.core._lexer._token import CrupyLexerToken
from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyLexerTokenSeq(CrupyLexerToken):
    """ sequence token information """
    seq: List[CrupyLexerToken]

class CrupyLexerSeq(CrupyLexer):
    """ execute sequence of lexer operation
    """
    def __init__(self, *args: Any) -> None:
        self._seq: List[CrupyLexer] = []
        for i, arg in enumerate(args):
            if CrupyLexer not in type(arg).mro():
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

    def __call__(self, stream: CrupyStream) -> CrupyLexerToken|None:
        """ execute all lexer operation
        """
        with stream as lexem:
            token_list: List[CrupyLexerToken] = []
            for lexer in self._seq:
                if not (token := lexer(stream)):
                    return None
                token_list.append(token)
            return CrupyLexerTokenSeq(
                stream_ctx  = lexem.validate(),
                seq         = token_list
            )
