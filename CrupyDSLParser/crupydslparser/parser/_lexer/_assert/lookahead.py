"""
crupydslparser.parser._lexer._assert.lookahead    - lookehader assert
"""
__all__ = [
    'CrupyLexerAssertLookaheadNegative',
    'CrupyLexerAssertLookaheadPositive',
]
from typing import Any

from crupydslparser.parser._lexer._assert.base import CrupyLexerAssertBase
from crupydslparser.parser._lexer._operation.base import CrupyLexerOpBase
from crupydslparser.parser.base import CrupyParserBase
from crupydslparser.parser.exception import CrupyParserBaseException
from crupydslparser.exception import CrupyDSLCoreException

#---
# Public
#---

class CrupyLexerAssertLookaheadNegative(CrupyLexerAssertBase):
    """ lexer lookahead negative operation
    """
    def __init__(self, *args: Any) -> None:
        super().__init__()
        self._seq: list[CrupyLexerOpBase] = []
        for i, arg in enumerate(args):
            if CrupyLexerOpBase not in type(arg).mro():
                raise CrupyDSLCoreException(
                    f"Unable to initialise the {type(self).__name__} "
                    f"because the argument {i} is not of type CrupyLexer "
                    f"({type(arg)})"
                )
            self._seq.append(arg)
        if not self._seq:
            raise CrupyDSLCoreException(
                f"Unable to initialise the {type(self).__name__} because "
                'not sequence has been presented'
            )

    def __call__(self, parser: CrupyParserBase) -> bool:
        """ return True of the lexer operation not match
        """
        with parser.stream as _:
            for lexer in self._seq:
                try:
                    lexer(parser)
                except CrupyParserBaseException:
                    return True
            return False

    #---
    # Public methods
    #---

    def show(self, indent: int = 0) -> str:
        """ display a generic information
        """
        content = f"{' ' * indent}{type(self).__name__}(\n"
        for alternative in self._seq:
            content += alternative.show(indent + 1)
            content += ',\n'
        content += f"{' ' * indent})"
        return content


class CrupyLexerAssertLookaheadPositive(CrupyLexerAssertLookaheadNegative):
    """ lexer lookahead negative operation
    """
    def __call__(self, parser: CrupyParserBase) -> bool:
        """ return True of the lexer operation not match
        """
        return not super().__call__(parser)
