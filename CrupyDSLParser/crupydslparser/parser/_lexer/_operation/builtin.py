"""
crupydslparser.parser._lexer._operation.builtin   - builtin operations
"""
__all__ = [
    'CrupyLexerOpBuiltin',
]

from crupydslparser.parser._lexer.exception import CrupyLexerException
from crupydslparser.parser._lexer._operation._base import CrupyLexerOpBase
from crupydslparser.parser._lexer._operation.text import (
    CrupyParserNodeLexText,
)
from crupydslparser.parser import (
    CrupyParserBase,
    CrupyParserNodeBase,
)

#---
# Public
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

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
            'space_nl',
            'eof',
        ]:
            raise CrupyLexerException(
                'Unable to configure the CrupyLexerOpBuiltin: '
                f"unrecognized operation '{operation}'"
            )
        self._operation = operation

    def __call__(self, parser: CrupyParserBase) -> CrupyParserNodeBase:
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
            'space_nl'       : self._is_space,
            'eof'            : self._is_end_of_file,
        }[self._operation](parser, self._operation)

    #---
    # Internals
    #---

    def _is_any(
        self,
        parser: CrupyParserBase,
        _: str,
    ) -> CrupyParserNodeBase:
        """ check any char
        """
        with parser.stream as context:
            if context.peek_char() == '\\':
                context.read_char()
            node: CrupyParserNodeBase|None = None
            for test in (
                (self._is_alphanum, 'alphanum'),
                (self._is_symbol, 'ascii'),
                (self._is_space, 'space_n'),
            ):
                try:
                    node = test[0](parser, test[1])
                    return CrupyParserNodeLexText(
                        context = context.validate(),
                        text    = node.text
                    )
                except CrupyLexerException:
                    pass
            self._raise_from_context(
                context,
                'Unable to validate the current char as "any"'
            )

    def _is_alphanum(
        self,
        parser: CrupyParserBase,
        target: str,
    ) -> CrupyParserNodeBase:
        """ check alphanum char
        """
        try:
            return self._is_number(parser, 'digit')
        except CrupyLexerException:
            pass
        if target in ['alphanum', 'alphanum_upper']:
            try:
                return self._is_alpha(parser, 'alpha_upper')
            except CrupyLexerException:
                pass
        if target != 'alphanum_upper':
            try:
                return self._is_alpha(parser, 'alpha_lower')
            except CrupyLexerException:
                pass
        with parser.stream as context:
            self._raise_from_context(
                context,
                f'Unable to validate the current char as "{target}"'
            )

    def _is_alpha(
        self,
        parser: CrupyParserBase,
        target: str,
    ) -> CrupyParserNodeBase:
        """ check if alphabet
        """
        with parser.stream as context:
            if not (curr := context.peek_char()):
                self._raise_from_context(
                    context,
                    'Unable to validate current char as "alpha", no stream '
                    'input available',
                )
            valid = 0
            if target in ['alpha', 'alpha_lower']:
                valid += bool('a' <= curr <= 'z')
            if target in ['alpha', 'alpha_upper']:
                valid += bool('A' <= curr <= 'Z')
            if valid == 0:
                self._raise_from_context(
                    context,
                    f'Unable to validate the current char as "{target}"',
                )
            context.read_char()
            return CrupyParserNodeLexText(
                context = context.validate(),
                text    = curr,
            )

    def _is_number(
        self,
        parser: CrupyParserBase,
        target: str,
    ) -> CrupyParserNodeBase:
        """ check if number or digit
        """
        with parser.stream as context:
            number = ''
            while True:
                if not (curr := context.peek_char()):
                    if number:
                        break
                    self._raise_from_context(
                        context,
                        'Unable to validate the current char as '
                        f"\"{target}\", no stream available",
                    )
                if not '0' <= curr <= '9':
                    break
                context.read_char()
                number += curr
                if target == 'digit':
                    break
            if not number:
                self._raise_from_context(
                    context,
                    f"Unable to validate the current char as \"{target}\"",
                )
            return CrupyParserNodeLexText(
                context = context.validate(),
                text    = number,
            )

    def _is_symbol(
        self,
        parser: CrupyParserBase,
        _: str,
    ) -> CrupyParserNodeBase:
        """ check if symbol
        """
        with parser.stream as context:
            if not (curr := context.peek_char()):
                self._raise_from_context(
                    context,
                    'Unable to validate the current char as "symbol", no '
                    'stream available',
                )
            if not curr in "|!#$%&()*+,-./:;>=<?@[\\]^_`{}~\"":
                self._raise_from_context(
                    context,
                    'Unable to validate the current char as "symbol"',
                )
            context.read_char()
            return CrupyParserNodeLexText(
                context = context.validate(),
                text    = curr,
            )

    def _is_space(
        self,
        parser: CrupyParserBase,
        target: str,
    ) -> CrupyParserNodeBase:
        """ check if space
        """
        with parser.stream as context:
            if not (curr := context.peek_char()):
                self._raise_from_context(
                    context,
                    'Unable to validate the current char as "space", no '
                    'stream available',
                )
            space_list = " \t" if target != 'space_nl' else " \t\r\n"
            if curr not in space_list:
                self._raise_from_context(
                    context,
                    f'Unable to validate the current char as "{target}"',
                )
            context.read_char()
            return CrupyParserNodeLexText(
                context = context.validate(),
                text    = curr,
            )

    def _is_end_of_file(
        self,
        parser: CrupyParserBase,
        _: str,
    ) -> CrupyParserNodeBase:
        """ check if space
        """
        with parser.stream as context:
            if context.peek_char():
                self._raise_from_context(
                    context,
                    'Unable to validate the current char as "EOF", '
                    'stream available',
                )
            return CrupyParserNodeLexText(
                context = context.validate(),
                text    = '',
            )
