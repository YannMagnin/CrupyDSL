"""
crupydslparser.parser._lexer._operation.rep  - zero or more lexer operation
"""
__all__ = [
    'CrupyParserNodeBaseLexRep',
    'CrupyLexerOpRep0N',
    'CrupyLexerOpRep1N',
]
from typing import Any

from crupydslparser.parser._lexer.exception import CrupyLexerException
from crupydslparser.parser._lexer._operation.seq import CrupyLexerOpSeq
from crupydslparser.parser import (
    CrupyParserBase,
    CrupyParserNodeBase,
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
    ) -> list[list[CrupyParserNodeBase]]:
        """ execute all lexer operation
        """
        rep: list[list[CrupyParserNodeBase]] = []
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

class CrupyParserNodeBaseLexRep(CrupyParserNodeBase):
    """ sequence token information """
    rep: list[list[CrupyParserNodeBase]]

## operations

class CrupyLexerOpRep0N(_CrupyLexerOpRepxN):
    """ required at least one repetition
    """
    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ execute lexer operation and require at least one sequence
        """
        with parser.stream as context:
            return CrupyParserNodeBaseLexRep(
                context = context.validate(),
                rep     = self._core_rep(parser),
            )

class CrupyLexerOpRep1N(_CrupyLexerOpRepxN):
    """ required at least one repetition
    """
    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
        """ execute lexer operation and require at least one sequence
        """
        with parser.stream as context:
            if len(req := self._core_rep(parser)) < 1:
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
            return CrupyParserNodeBaseLexRep(
                context = context.validate(),
                rep     = req,
            )