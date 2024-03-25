"""
crupydslparser.core._lexer.exception     - lexer exception class
"""
# allow returning `CrupyLexerException` in class methods prototype since
# the type, as the time where CPython analyse the class, do not "really"
# exists
from __future__ import annotations

__all__ = [
    'CrupyLexerException',
]

from crupydslparser.core.exception import CrupyDSLCoreException
from crupydslparser.core.parser import CrupyParserBase

#---
# Public
#---

class CrupyLexerException(CrupyDSLCoreException):
    """ Crupy lexer exception class """

    #---
    # Utilities
    #---

    @classmethod
    def from_operation(
        cls,
        parser: CrupyParserBase,
    ) -> CrupyLexerException:
        """ generate syntax error exception
        """
        return cls(
            f"Parsing exception occured:\n"
            '\n'
            f"{parser.stream.generate_error_context()}\n"
            '\n'
            'SyntaxError: invalid syntax (unable to find appropriate '
            'production to parse this stream here)'
        )
