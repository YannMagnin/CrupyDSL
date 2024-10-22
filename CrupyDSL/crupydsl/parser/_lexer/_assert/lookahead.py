"""
crupydsl.parser._lexer._assert.lookahead    - lookehader assert
"""
__all__ = [
    'CrupyDSLLexerAssertLookaheadNegative',
    'CrupyDSLLexerAssertLookaheadPositive',
]
from typing import Any

from crupydsl.parser._lexer._assert.base import CrupyDSLLexerAssertBase
from crupydsl.parser._lexer._operation.op_base import CrupyDSLLexerOpBase
from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyDSLLexerAssertLookaheadNegative(CrupyDSLLexerAssertBase):
    """ lexer lookahead negative operation
    """
    def __init__(self, *args: Any) -> None:
        super().__init__()
        self._seq: list[CrupyDSLLexerOpBase] = []
        for i, arg in enumerate(args):
            if CrupyDSLLexerOpBase not in type(arg).mro():
                raise CrupyDSLCoreException(
                    f"Unable to initialise the {type(self).__name__} "
                    f"because the argument {i} is not of type CrupyDSLLexer "
                    f"({type(arg)})"
                )
            self._seq.append(arg)
        if not self._seq:
            raise CrupyDSLCoreException(
                f"Unable to initialise the {type(self).__name__} because "
                'not sequence has been presented'
            )

    def __call__(self, parser: CrupyDSLParserBase) -> bool:
        """ return True of the lexer operation not match
        """
        with parser.stream as _:
            for lexer in self._seq:
                try:
                    lexer(parser)
                except CrupyDSLParserBaseException:
                    return True
            return False

    #---
    # Public methods
    #---

    def debug_show(self, indent: int = 0) -> str:
        """ display a generic information
        """
        content = f"{' ' * indent}{type(self).__name__}(\n"
        for alternative in self._seq:
            content += alternative.debug_show(indent + 1)
            content += ',\n'
        content += f"{' ' * indent})"
        return content


class CrupyDSLLexerAssertLookaheadPositive(
    CrupyDSLLexerAssertLookaheadNegative
):
    """ lexer lookahead negative operation
    """
    def __call__(self, parser: CrupyDSLParserBase) -> bool:
        """ return True of the lexer operation not match
        """
        return not super().__call__(parser)
