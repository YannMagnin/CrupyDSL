"""
crupydslparser.core._lexer._operation.rep  - zero or more lexer operation
"""
__all__ = (
    'CrupyParserNodeLexRep',
    'CrupyLexerOpRep0N',
    'CrupyLexerOpRep1N',
)
from typing import Any

from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core._lexer._operation.seq import CrupyLexerOpSeq
from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Internals
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238
class _CrupyLexerOpRepxN(CrupyLexerOpSeq):
    """ execute sequence of lexer operation
    """
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self._error: CrupyLexerException|None = None

    #---
    # Internals
    #---

    def _core_rep(
        self,
        parser: CrupyParserBase,
    ) -> list[list[CrupyParserNode]]:
        """ execute all lexer operation
        """
        rep: list[list[CrupyParserNode]] = []
        while True:
            with parser.stream as context:
                try:
                    rep.append(super().__call__(parser).seq)
                    context.validate()
                except CrupyLexerException as err:
                    self._error = err
                    return rep

#---
# Public
#---

## nodes

class CrupyParserNodeLexRep(CrupyParserNode):
    """ sequence token information """
    rep: list[list[CrupyParserNode]]

## operations

class CrupyLexerOpRep0N(_CrupyLexerOpRepxN):
    """ required at least one repetition
    """
    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode:
        """ execute lexer operation and require at least one sequence
        """
        with parser.stream as context:
            return CrupyParserNodeLexRep(
                context = context.validate(),
                rep     = self._core_rep(parser),
            )

class CrupyLexerOpRep1N(_CrupyLexerOpRepxN):
    """ required at least one repetition
    """
    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode:
        """ execute lexer operation and require at least one sequence
        """
        with parser.stream as context:
            if len(req := self._core_rep(parser)) >= 1:
                return CrupyParserNodeLexRep(
                    context = context.validate(),
                    rep     = req,
                )
            if not self._error:
                raise CrupyLexerException(
                    f"{type(self).__name__}: "
                    'Missing critical error information'
                )
            self._raise_from_context(
                self._error.context,
                'Unable to perform at least one repetition of the '
                'sequence. Reason:\n'
                f"{self._error.reason}"
            )
