"""
crupydslparser.parser._lexer.exception  - lexer exception class
"""
# allow returning `CrupyLexerException` in class methods prototype since
# the type, as the time where CPython analyse the class, do not "really"
# exists
from __future__ import annotations

__all__ = [
    'CrupyParserLexerException',
]

from crupydslparser.parser.exception import CrupyParserBaseException
#from crupydslparser.parser._stream import CrupyStreamContext

#---
# Public
#---

class CrupyParserLexerException(CrupyParserBaseException):
    """ Crupy lexer exception class """

    #@classmethod
    #def from_context(
    #    cls,
    #    context: CrupyStreamContext,
    #    error: str,
    #) -> NoReturn:
    #    """ raise generic lexer operation exception
    #    """
    #    raise CrupyLexerException(
    #        message = f"{type(self).__name__}: {error}",
    #        context = context,
    #    )
