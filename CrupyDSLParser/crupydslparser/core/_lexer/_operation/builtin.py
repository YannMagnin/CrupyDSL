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
        return {
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
        }[self._operation](parser, self._operation)


    #---
    # Internals
    #---

    def _is_any(
        self,
        parser: CrupyParserBase,
        _: str,
    ) -> CrupyParserNode|None:
        """ check any char
        """
        with parser.stream as lexem:
            if lexem.peek_char() == '\\':
                lexem.read_char()
            while True:
                if node := self._is_alphanum(parser, 'alphanum'):
                    break
                if node := self._is_symbol(parser, 'ascii'):
                    break
                if node := self._is_space(parser, 'space_n'):
                    break
                return None
            lexem.validate()
            return node

    def _is_alphanum(
        self,
        parser: CrupyParserBase,
        target: str,
    ) -> CrupyParserNode|None:
        """ check alphanum char
        """
        if node := self._is_number(parser, 'digit'):
            return node
        if target in ['alphanum', 'alphanum_upper']:
            if node := self._is_alpha(parser, 'alpha_upper'):
                return node
        return self._is_alpha(parser, 'alpha_lower')

    def _is_alpha(
        self,
        parser: CrupyParserBase,
        target: str,
    ) -> CrupyParserNode|None:
        """ check if alphabet
        """
        with parser.stream as lexem:
            if not (curr := lexem.read_char()):
                return None
            valid = 0
            if target in ['alpha', 'alpha_lower']:
                valid += bool('a' <= curr <= 'z')
            if target in ['alpha', 'alpha_upper']:
                valid += bool('A' <= curr <= 'Z')
            if valid == 0:
                return None
            return CrupyParserNodeLexText(
                stream_ctx  = lexem.validate(),
                text        = curr,
            )

    def _is_number(
        self,
        parser: CrupyParserBase,
        target: str,
    ) -> CrupyParserNode|None:
        """ check if number or digit
        """
        with parser.stream as lexem:
            number = ''
            while True:
                if not (curr := lexem.peek_char()):
                    return None
                if not '0' <= curr <= '9':
                    break
                lexem.read_char()
                number += curr
                if target == 'digit':
                    break
            if not number:
                return None
            return CrupyParserNodeLexText(
                stream_ctx  = lexem.validate(),
                text        = number,
            )

    def _is_symbol(
        self,
        parser: CrupyParserBase,
        _: str,
    ) -> CrupyParserNode|None:
        """ check if symbol
        """
        with parser.stream as lexem:
            if not (curr := lexem.peek_char()):
                return None
            if not curr in "| !#$%&()*+,-./:;>=<?@[\\]^_`{}~\"":
                return None
            return CrupyParserNodeLexText(
                stream_ctx  = lexem.validate(),
                text        = lexem.read_char(),
            )

    def _is_space(
        self,
        parser: CrupyParserBase,
        target: str,
    ) -> CrupyParserNode|None:
        """ check if space
        """
        with parser.stream as lexem:
            if not (curr := lexem.peek_char()):
                return None
            space_list = " \t\v"
            if target == 'space_n':
                space_list = " \t\v\r\n"
            if curr not in space_list:
                return None
            return CrupyParserNodeLexText(
                stream_ctx  = lexem.validate(),
                text        = lexem.read_char(),
            )
