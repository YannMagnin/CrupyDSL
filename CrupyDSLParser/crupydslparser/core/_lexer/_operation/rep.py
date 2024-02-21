"""
crupydslparser.core._lexer._operation.rep0  - zero or more lexer operation
"""
__all__ = [
    'CrupyParserNodeLexRep',
    'CrupyLexerOpRep0N',
    'CrupyLexerOpRep1N',
]
from typing import List, Any, cast

from crupydslparser.core._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.core._lexer._assert._base import CrupyLexerAssertBase
from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Internals
#---

# Allow to fiew public methods
# pylint: disable=locally-disabled,R0903

class _CrupyLexerOpRepxN(CrupyLexerOpBase):
    """ execute sequence of lexer operation
    """
    def __init__(self, *args: Any) -> None:
        self._seq: List[CrupyLexerOpBase|CrupyLexerAssertBase] = []
        for i, arg in enumerate(args):
            if (
                    CrupyLexerOpBase not in type(arg).mro()
                and CrupyLexerAssertBase not in type(arg).mro()
            ):
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
        parser: CrupyParserBase,
    ) -> List[List[CrupyParserNode]]:
        """ execute all lexer operation
        """
        rep: List[List[CrupyParserNode]] = []
        while True:
            with parser.stream as lexem:
                valid = True
                token_list: List[CrupyParserNode] = []
                for lexer in self._seq:
                    if issubclass(type(lexer), CrupyLexerAssertBase):
                        if lexer(parser):
                            continue
                    else:
                        if token := lexer(parser):
                            token_list.append(
                                cast(CrupyParserNode, token),
                            )
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

## nodes

class CrupyParserNodeLexRep(CrupyParserNode):
    """ sequence token information """
    rep: List[List[CrupyParserNode]]

## operations

class CrupyLexerOpRep0N(_CrupyLexerOpRepxN):
    """ required at least one repetition
    """
    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode|None:
        """ execute lexer operation and require at least one sequence
        """
        with parser.stream as lexem:
            return CrupyParserNodeLexRep(
                stream_ctx  = lexem.validate(),
                rep         = self._core_rep(parser),
            )

class CrupyLexerOpRep1N(_CrupyLexerOpRepxN):
    """ required at least one repetition
    """
    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode|None:
        """ execute lexer operation and require at least one sequence
        """
        with parser.stream as lexem:
            if len(req := self._core_rep(parser)) < 1:
                return None
            return CrupyParserNodeLexRep(
                stream_ctx  = lexem.validate(),
                rep         = req,
            )
