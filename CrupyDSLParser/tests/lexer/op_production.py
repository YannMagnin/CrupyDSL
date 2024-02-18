"""
tests.lexer.op_production   - test the CrupyLexerProduction
"""
__all__ = [
    'CrupyUnittestLexerProd'
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core.parser._test import CrupyParserTest
from crupydslparser.core.parser.exception import CrupyParserException
from crupydslparser.core._lexer import (
    CrupyLexerProduction,
    CrupyLexerText,
)

#---
# Public
#---

class CrupyUnittestLexerProd(CrupyUnittestBase):
    """ unittest suite for the crupy lexer production calling operation
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple success test """
        parser = CrupyParserTest(
            production_test     = '\tabcdef ijkl',
            production_book     = {
                'entry'  : CrupyLexerProduction('entry2'),
                'entry2' : CrupyLexerText('abcdef')
            },
        )
        test = parser.execute('entry')
        self.assertIsNotNone(test)
        if test is None:
            return
        self.assertEqual(test['text'], 'abcdef')
        with parser.stream as lexem:
            self.assertEqual(lexem.read(), 'ijkl')

    def test_raise_error(self) -> None:
        """ force production calling that not exists """
        parser = CrupyParserTest(
            production_test     = '\tabcdef ijkl',
            production_book     = {
                'entry'  : CrupyLexerProduction('entry2'),
            },
        )
        self.assertRaises(
            exc_obj     = CrupyParserException(
                'Unable to find the primary production entry name '
                '\'entry2\''
            ),
            request     = (parser, 'execute', 'entry'),
        )
