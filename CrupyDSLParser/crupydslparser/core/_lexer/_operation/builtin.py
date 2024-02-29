"""
crupydslparser.core._lexer._operation.builtin   - builtin operations
"""
__all__ = [
    'CrupyLexerOpBuiltin',
]

from crupydslparser.core._stream.lexem import CrupyStreamLexem
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
            'number',
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
            text = {
                'any'            : self._is_any,
                'alphanum'       : self._is_alphanum,
                'alphanum_upper' : self._is_alphanum,
                'alphanum_lower' : self._is_alphanum,
                'alpha'          : self._is_alpha,
                'alpha_lower'    : self._is_alpha,
                'alpha_upper'    : self._is_alpha,
                'digit'          : self._is_number,
                'number'         : self._is_number,
                'symbol'         : self._is_symbol,
                'space'          : self._is_space,
                'space_n'        : self._is_space,
            }[self._operation](lexem, self._operation)
            if not text:
                return None
            return CrupyParserNodeLexText(
                stream_ctx  = lexem.validate(),
                text        = text,
            )

    #---
    # Internals
    #---

    def _is_any(self, lexem: CrupyStreamLexem, _: str) -> str|None:
        """ check any char
        """
        if text := self._is_alphanum(lexem, 'alphanum'):
            return text
        if text := self._is_number(lexem, 'decimal'):
            return text
        if text:= self._is_symbol(lexem, 'ascii'):
            return text
        if text := self._is_space(lexem, 'space_n'):
            return text
        return None

    def _is_alphanum(
        self,
        lexem: CrupyStreamLexem,
        target: str,
    ) -> str|None:
        """ check alphanum char
        """
        if text := self._is_number(lexem, 'decimal'):
            return text
        if target in ['alphanum', 'alphanum_upper']:
            if text := self._is_alpha(lexem, 'alpha_upper'):
                return text
        return self._is_alpha(lexem, 'alpha_lower')

    def _is_alpha(self, lexem: CrupyStreamLexem, target: str) -> str|None:
        """ check if alphabet
        """
        if not (curr := lexem.read_char()):
            return None
        if target in ['alpha', 'alpha_lower'] and bool('a' <= curr <= 'z'):
            return curr
        if target in ['alpha', 'alpha_upper'] and bool('A' <= curr <= 'Z'):
            return curr
        return None

    def _is_number(self, lexem: CrupyStreamLexem, target: str) -> str|None:
        """ check if number or digit
        """
        number = ''
        while True:
            if not (curr := lexem.read_char()):
                return None
            if not '0' <= curr <= '9':
                return number
            number += curr
            if target == 'digit':
                return number

    def _is_symbol(self, lexem: CrupyStreamLexem, _: str) -> str|None:
        """ check if symbol
        """
        if not (curr := lexem.read_char()):
            return None
        if curr in r"| !#$%&()*+,-./:;>=<?@[\]^_`{}~":
            return curr
        return None

    def _is_space(self, lexem: CrupyStreamLexem, target: str) -> str|None:
        """ check if space
        """
        if not (curr := lexem.read_char()):
            return None
        if target == 'space_n':
            return curr if curr in " \t\v\n" else None
        return curr if curr in " \t\v" else None
