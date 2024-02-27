"""
crupydslparser.core._lexer._operation.builtin   - builtin operations
"""
__all__ = [
    'CrupyLexerOpBuiltin',
]

from crupydslparser.core._lexer.exception import CrupyLexerException
from crupydslparser.core._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.core._lexer._operation.text import (
    CrupyParserNodeLexText,
)
from crupydslparser.core.parser import (
    CrupyParserBase,
    CrupyParserNode,
)

#---
# Public
#---

class CrupyLexerOpBuiltin(CrupyLexerOpBase):
    """ builtin operations
    """
    def __init__(self, operation: str) -> None:
        if operation not in [
            'any',
            'alphanum',
            'alphanum_lower',
            'alphanum_upper',
            'alpha',
            'alpha_upper',
            'alpha_lower',
            'digit',
            'symbol',
            'space',
            'space_n',
        ]:
            raise CrupyLexerException(
                'Unable to configure the CrupyLexerOpBuiltin: '
                f"unrecognized operation '{operation}'"
            )
        self._operation = operation

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNode|None:
        """ handle builtin
        """
        with parser.stream as lexem:
            if not (curr := lexem.read_char()):
                return None
            valid = {
                'any'            : self._is_any,
                'alphanum'       : self._is_alphanum,
                'alphanum_upper' : self._is_alphanum,
                'alphanum_lower' : self._is_alphanum,
                'alpha'          : self._is_alpha,
                'alpha_lower'    : self._is_alpha,
                'alpha_upper'    : self._is_alpha,
                'digit'          : self._is_digit,
                'symbol'         : self._is_symbol,
                'space'          : self._is_space,
                'space_n'        : self._is_space,
            }[self._operation](curr, self._operation)
            if not valid:
                return None
            return CrupyParserNodeLexText(
                stream_ctx  = lexem.validate(),
                text        = curr,
            )

    #---
    # Internals
    #---

    def _is_any(self, curr: str, _: str) -> bool:
        """ check any char
        """
        return (
               self._is_alphanum(curr, 'alphanum')
            or self._is_digit(curr, 'decimal')
            or self._is_symbol(curr, 'ascii')
        )

    def _is_alphanum(self, curr: str, target: str) -> bool:
        """ check alphanum char
        """
        if self._is_digit(curr, 'decimal'):
            return True
        if target in ['alphanum', 'alphanum_upper']:
            if self._is_alpha(curr, 'alpha_upper'):
                return True
        return self._is_alpha(curr, 'alpha_lower')

    def _is_alpha(self, curr: str, target: str) -> bool:
        """ check if alphabet
        """
        valid = 0
        if target in ['alpha', 'alpha_lower']:
            valid +=  bool('a' <= curr <= 'z')
        if target in ['alpha', 'alpha_upper']:
            valid += bool('A' <= curr <= 'Z')
        return bool(valid)

    def _is_digit(self, curr: str, _: str) -> bool:
        """ check if digit
        """
        return bool('0' <= curr <= '9')

    def _is_symbol(self, curr: str, _: str) -> bool:
        """ check if symbol
        """
        return bool(curr in r"| !#$%&()*+,-./:;>=<?@[\]^_`{}~")

    def _is_space(self, curr: str, target: str) -> bool:
        """ check if space
        """
        if target == 'space_n':
            return bool(curr in " \t\v\n")
        return bool(curr in " \t\v")
