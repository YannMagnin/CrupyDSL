"""
crupydslparser.core._lexer.op_rep0  - zero or more lexer operation
"""
__all__ = [
    'CrupyLexerRep0N',
]
from typing import List, Any

from crupydslparser.core._lexer._lexer import CrupyLexer
from crupydslparser.core._lexer._token import CrupyLexerToken
from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core._stream import CrupyStream

#---
# Internals
#---

# Allow to fiew public methods
# pylint: disable=locally-disabled,R0903

class _CrupyLexerRepxN(CrupyLexer):
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

    #---
    # Internals
    #---

    def _core_rep(
        self,
        stream: CrupyStream,
    ) -> List[List[CrupyLexerToken]]:
        """ execute all lexer operation
        """
        rep: List[List[CrupyLexerToken]] = []
        while True:
            with stream as lexem:
                valid = True
                token_list: List[CrupyLexerToken] = []
                for lexer in self._seq:
                    if token := lexer(stream):
                        token_list.append(token)
                        continue
                    valid = False
                    break
                if not valid:
                    break
                rep.append(token_list)
                lexem.validate()
        return rep

#---
# Public
#---

class CrupyLexerTokenRep(CrupyLexerToken):
    """ sequence token information """
    rep: List[List[CrupyLexerToken]]

class CrupyLexerRep0N(_CrupyLexerRepxN):
    """ required at least one repetition
    """
    def __call__(self, stream: CrupyStream) -> CrupyLexerToken|None:
        """ execute lexer operation and require at least one sequence
        """
        with stream as lexem:
            return CrupyLexerTokenRep(
                stream_ctx  = lexem.validate(),
                rep         = self._core_rep(stream),
            )

class CrupyLexerRep1N(_CrupyLexerRepxN):
    """ required at least one repetition
    """
    def __call__(self, stream: CrupyStream) -> CrupyLexerToken|None:
        """ execute lexer operation and require at least one sequence
        """
        with stream as lexem:
            if len(req := self._core_rep(stream)) < 1:
                return None
            return CrupyLexerTokenRep(
                stream_ctx  = lexem.validate(),
                rep         = req,
            )
