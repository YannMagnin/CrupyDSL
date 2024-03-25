"""
crupydslparser.core._lexer._operation.rep0  - zero or more lexer operation
"""
__all__ = [
    'CrupyParserNodeLexRep',
    'CrupyLexerOpRep0N',
    'CrupyLexerOpRep1N',
]
from typing import List

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

    #---
    # Internals
    #---

    def _core_rep(
        self,
        parser: CrupyParserBase,
        last_chance: bool,
    ) -> List[List[CrupyParserNode]]:
        """ execute all lexer operation
        """
        rep: List[List[CrupyParserNode]] = []
        while True:
            with parser.stream as lexem:
                if not (node := super()._execute(parser, last_chance)):
                    break
                rep.append(node.seq)
                lexem.validate()
        return rep

#---
# Public
#---

## nodes

class CrupyParserNodeLexRep(CrupyParserNode):
    """ sequence token information """
    rep: List[List[CrupyParserNode]]

## operations

class CrupyLexerOpRep0N(_CrupyLexerOpRepxN):
    """ required at least one repetition
    """
    def _execute(
        self,
        parser: CrupyParserBase,
        _: bool,
    ) -> CrupyParserNode|None:
        """ execute lexer operation and require at least one sequence
        """
        with parser.stream as lexem:
            return CrupyParserNodeLexRep(
                stream_ctx  = lexem.validate(),
                rep         = self._core_rep(parser, False),
            )

class CrupyLexerOpRep1N(_CrupyLexerOpRepxN):
    """ required at least one repetition
    """
    def _execute(
        self,
        parser: CrupyParserBase,
        last_chance: bool,
    ) -> CrupyParserNode|None:
        """ execute lexer operation and require at least one sequence
        """
        with parser.stream as lexem:
            if len(req := self._core_rep(parser, last_chance)) < 1:
                return None
            return CrupyParserNodeLexRep(
                stream_ctx  = lexem.validate(),
                rep         = req,
            )
