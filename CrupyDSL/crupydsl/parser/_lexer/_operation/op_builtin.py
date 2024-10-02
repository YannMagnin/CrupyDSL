"""
crupydsl.parser._lexer._operation.builtin   - builtin operations
"""
__all__ = [
    'CrupyDSLLexerOpBuiltin',
    'CrupyDSLLexerOpBuiltinException',
    'CrupyDSLParserNodeBuiltinEof',
]
from typing import cast

from crupydsl.parser._lexer.exception import CrupyDSLLexerException
from crupydsl.parser._lexer._operation.op_base import CrupyDSLLexerOpBase
from crupydsl.parser._lexer._operation.op_text import (
    CrupyDSLParserNodeLexText,
)
from crupydsl.parser.base import CrupyDSLParserBase
from crupydsl.parser.node import CrupyDSLParserNodeBase
from crupydsl.exception import CrupyDSLCoreException

#---
# Public
#---

# allow to few methods and unused private methods
# pylint: disable=locally-disabled,R0903,W0238

class CrupyDSLLexerOpBuiltinException(CrupyDSLLexerException):
    """ exception class """

class CrupyDSLParserNodeBuiltinEof(CrupyDSLParserNodeBase):
    """ special end-of-file node """

class CrupyDSLLexerOpBuiltin(CrupyDSLLexerOpBase):
    """ builtin operations
    """
    def __init__(self, operation: str) -> None:
        super().__init__()
        if operation not in [
            'any',
            'any_newline',
            'alphanum',
            'alphanum_lower',
            'alphanum_upper',
            'alpha',
            'alpha_upper',
            'alpha_lower',
            'digit',
            'number',
            'newline',
            'symbol',
            'space',
            'space_newline',
            'spaces',
            'spaces_newline',
            'eof',
        ]:
            raise CrupyDSLCoreException(
                'Unable to configure the CrupyDSLLexerOpBuiltin: '
                f"unrecognized operation '{operation}'"
            )
        self._operation = operation

    def __call__(self, parser: CrupyDSLParserBase) -> CrupyDSLParserNodeBase:
        """ handle builtin
        """
        return {
            'any'            : self._is_any,
            'any_newline'    : self._is_any,
            'alphanum'       : self._is_alphanum,
            'alphanum_upper' : self._is_alphanum,
            'alphanum_lower' : self._is_alphanum,
            'alpha'          : self._is_alpha,
            'alpha_lower'    : self._is_alpha,
            'alpha_upper'    : self._is_alpha,
            'digit'          : self._is_number,
            'number'         : self._is_number,
            'newline'        : self._is_newline,
            'symbol'         : self._is_symbol,
            'space'          : self._is_space,
            'space_newline'  : self._is_space,
            'spaces'         : self._is_space,
            'spaces_newline' : self._is_space,
            'eof'            : self._is_end_of_file,
        }[self._operation](parser, self._operation)

    #---
    # Internals
    #---

    def _is_any(
        self,
        parser: CrupyDSLParserBase,
        target: str,
    ) -> CrupyDSLParserNodeBase:
        """ check any char

        @notes
        - by default, if the current char is a backslash, ignore read the
            next char. This is a poor support for the escape handling, but
            can have collision with new line maybe (e.g. '\\\n')
            (todo)
        """
        with parser.stream as context:
            if context.peek_char() == '\\':
                context.read_char()
            for i, test in enumerate((
                (self._is_newline, ''),
                (self._is_alphanum, 'alphanum'),
                (self._is_symbol, 'ascii'),
                (self._is_space, 'space'),
            )):
                try:
                    if i == 0 and target != 'any_newline':
                        continue
                    node = test[0](parser, test[1])
                    return CrupyDSLParserNodeLexText(
                        context = context.validate(),
                        text    = node.text,
                    )
                except CrupyDSLLexerException:
                    pass
            raise CrupyDSLLexerOpBuiltinException(
                context = context,
                reason  = \
                    f"unable to validate the current char as \"{target}\"",
            )

    def _is_alphanum(
        self,
        parser: CrupyDSLParserBase,
        target: str,
    ) -> CrupyDSLParserNodeBase:
        """ check alphanum char
        """
        try:
            return self._is_number(parser, 'digit')
        except CrupyDSLLexerException:
            pass
        if target in ['alphanum', 'alphanum_upper']:
            try:
                return self._is_alpha(parser, 'alpha_upper')
            except CrupyDSLLexerException:
                pass
        if target != 'alphanum_upper':
            try:
                return self._is_alpha(parser, 'alpha_lower')
            except CrupyDSLLexerException:
                pass
        with parser.stream as context:
            raise CrupyDSLLexerOpBuiltinException(
                context = context,
                reason  = \
                    f'unable to validate the current char as "{target}"'
            )

    def _is_alpha(
        self,
        parser: CrupyDSLParserBase,
        target: str,
    ) -> CrupyDSLParserNodeBase:
        """ check if alphabet
        """
        with parser.stream as context:
            if not (curr := context.peek_char()):
                raise CrupyDSLLexerOpBuiltinException(
                    context = context,
                    reason  = \
                        'unable to validate current char as "alpha", no '
                        'stream input available',
                )
            valid = 0
            if target in ['alpha', 'alpha_lower']:
                valid += bool('a' <= curr <= 'z')
            if target in ['alpha', 'alpha_upper']:
                valid += bool('A' <= curr <= 'Z')
            if valid == 0:
                raise CrupyDSLLexerOpBuiltinException(
                    context = context,
                    reason  = \
                        'unable to validate the current char as '
                        f"\"{target}\"",
                )
            context.read_char()
            return CrupyDSLParserNodeLexText(
                context = context.validate(),
                text    = curr,
            )

    def _is_number(
        self,
        parser: CrupyDSLParserBase,
        target: str,
    ) -> CrupyDSLParserNodeBase:
        """ check if number or digit
        """
        with parser.stream as context:
            number = ''
            while True:
                if not (curr := context.peek_char()):
                    if number:
                        break
                    raise CrupyDSLLexerOpBuiltinException(
                        context = context,
                        reason  = \
                            'unable to validate the current char as '
                            f"\"{target}\", no stream available",
                    )
                if not '0' <= curr <= '9':
                    break
                context.read_char()
                number += curr
                if target == 'digit':
                    break
            if not number:
                raise CrupyDSLLexerOpBuiltinException(
                    context = context,
                    reason  = \
                        'unable to validate the current char as '
                        f"\"{target}\"",
                )
            return CrupyDSLParserNodeLexText(
                context = context.validate(),
                text    = number,
            )

    def _is_newline(
        self,
        parser: CrupyDSLParserBase,
        _: str,
    ) -> CrupyDSLParserNodeBase:
        """ check if newline
        """
        with parser.stream as context:
            if not (curr := context.peek_char()):
                raise CrupyDSLLexerOpBuiltinException(
                    context = context,
                    reason  = \
                        'unable to validate the current char as '
                        '"newline", no stream available',
                )
            if curr not in ('\n', '\r\n'):
                raise CrupyDSLLexerOpBuiltinException(
                    context = context,
                    reason  = \
                        'unable to validate the current char as "newline"',
                )
            context.read_char()
            return CrupyDSLParserNodeLexText(
                context = context.validate(),
                text    = curr,
            )

    def _is_symbol(
        self,
        parser: CrupyDSLParserBase,
        _: str,
    ) -> CrupyDSLParserNodeBase:
        """ check if symbol
        """
        with parser.stream as context:
            if not (curr := context.peek_char()):
                raise CrupyDSLLexerOpBuiltinException(
                    context = context,
                    reason  = \
                        'unable to validate the current char as '
                        '"symbol", no stream available',
                )
            if not curr in "|!#$%&()*+,-./:;>=<?@[\\]^_`{}~\"'\r":
                raise CrupyDSLLexerOpBuiltinException(
                    context = context,
                    reason  = \
                        'unable to validate the current char as "symbol"',
                )
            context.read_char()
            return CrupyDSLParserNodeLexText(
                context = context.validate(),
                text    = curr,
            )

    def _is_space(
        self,
        parser: CrupyDSLParserBase,
        target: str,
    ) -> CrupyDSLParserNodeBase:
        """ check space builtin

        @notes
        - target='space' -> only if the current char is space or tab
        - target='space_newline' -> same as 'space' but check newline too
        - target='spaces' -> at least one space or tab and loop
        - target='spaces_newline' -> same as 'spaces' but check newline too
        """
        with parser.stream as context:
            capture = ''
            while True:
                if not (curr := context.peek_char()):
                    raise CrupyDSLLexerOpBuiltinException(
                        context = context,
                        reason  = \
                            'unable to validate the current char as '
                            '"space", no stream available',
                    )
                if curr not in ' \t':
                    try:
                        found = False
                        if target in ('space_newline', 'spaces_newline'):
                            curr = self._is_newline(parser, '').text
                            found = True
                    except CrupyDSLLexerOpBuiltinException:
                        pass
                    if not found:
                        if capture:
                            break
                        raise CrupyDSLLexerOpBuiltinException(
                            context = context,
                            reason  = \
                                'unable to validate the current char as '
                                f"\"{target}\"",
                        )
                else:
                    context.read_char()
                capture += cast(str, curr)
                if target in ('space', 'space_newline'):
                    break
            return CrupyDSLParserNodeLexText(
                context = context.validate(),
                text    = capture,
            )

    def _is_end_of_file(
        self,
        parser: CrupyDSLParserBase,
        _: str,
    ) -> CrupyDSLParserNodeBase:
        """ check if space
        """
        with parser.stream as context:
            if context.peek_char():
                raise CrupyDSLLexerOpBuiltinException(
                    context = context,
                    reason  = \
                        'unable to validate the current char as "EOF", '
                        'stream available',
                )
            return CrupyDSLParserNodeBuiltinEof(
                context = context.validate(),
            )

    #---
    # Public methods
    #---

    def show(self, indent: int = 0) -> str:
        """ display a generic information
        """
        return f"{' ' * indent}{type(self).__name__}('{self._operation}')"
