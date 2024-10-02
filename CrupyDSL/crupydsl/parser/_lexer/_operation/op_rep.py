"""
crupydsl.parser._lexer._operation.rep  - zero or more lexer operation
"""
__all__ = [
    'CrupyDSLParserNodeLexRep',
    'CrupyDSLLexerOpRep0N',
    'CrupyDSLLexerOpRep1N',
    'CrupyDSLLexerOpRepException',
]
from typing import Union, Any

from crupydsl.parser._lexer.exception import CrupyDSLLexerException
from crupydsl.parser._lexer._operation.op_seq import (
    CrupyDSLLexerOpSeq,
    CrupyDSLLexerOpSeqException,
)
from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser.node import CrupyDSLParserNodeBase

#---
# Internals
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

class _CrupyDSLLexerOpRepxN(CrupyDSLLexerOpSeq):
    """ execute sequence of lexer operation
    """
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self._error: Union[CrupyDSLLexerOpSeqException,None] = None

    #---
    # Internals
    #---

    def _core_rep(
        self,
        parser: CrupyDSLParserBase,
    ) -> list[list[CrupyDSLParserNodeBase]]:
        """ execute all lexer operation
        """
        rep: list[list[CrupyDSLParserNodeBase]] = []
        while True:
            with parser.stream as context:
                try:
                    rep.append(super().__call__(parser).seq)
                    context.validate()
                except CrupyDSLLexerOpSeqException as err:
                    self._error = err
                    break
        return rep

#---
# Public
#---

## nodes

class CrupyDSLParserNodeLexRep(CrupyDSLParserNodeBase):
    """ sequence token information """
    rep: list[list[CrupyDSLParserNodeBase]]

class CrupyDSLLexerOpRepException(CrupyDSLLexerException):
    """ exception class """
    validated_step: int

## operations

class CrupyDSLLexerOpRep0N(_CrupyDSLLexerOpRepxN):
    """ required at least one repetition
    """
    def __call__(self, parser: CrupyDSLParserBase) -> CrupyDSLParserNodeBase:
        """ execute lexer operation and require at least one sequence
        """
        with parser.stream as context:
            return CrupyDSLParserNodeLexRep(
                context = context.validate(),
                rep     = self._core_rep(parser),
            )

class CrupyDSLLexerOpRep1N(_CrupyDSLLexerOpRepxN):
    """ required at least one repetition
    """
    def __call__(self, parser: CrupyDSLParserBase) -> CrupyDSLParserNodeBase:
        """ execute lexer operation and require at least one sequence
        """
        with parser.stream as context:
            if len(req := self._core_rep(parser)) >= 1:
                return CrupyDSLParserNodeLexRep(
                    context = context.validate(),
                    rep     = req,
                )
            if self._error:
                raise CrupyDSLLexerOpRepException(
                    context         = self._error.context,
                    validated_step  = self._error.validated_operation,
                    reason          = self._error.reason,
                    message         = self._error.message,
                )
            raise CrupyDSLLexerOpRepException(
                context         = context,
                validated_step  = 0,
                reason          = 'missing critical error information',
            )
