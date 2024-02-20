"""
tests.lexer.op_production   - test the CrupyLexerOpProduction
"""
__all__ = [
    'CrupyUnittestLexerProd'
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core.parser._base import CrupyParserBase
from crupydslparser.core.parser.exception import CrupyParserException
from crupydslparser.core._lexer import (
    CrupyLexerOpProductionCall,
    CrupyLexerOpText,
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
        parser = CrupyParserBase({
            'entry'  : CrupyLexerOpProductionCall('entry2'),
            'entry2' : CrupyLexerOpText('abcdef')
        })
        test = parser.execute('entry', '\tabcdef ijkl')
        self.assertIsNotNone(test)
        if test is None:
            return
        self.assertEqual(test['text'], 'abcdef')
        with parser.stream as lexem:
            self.assertEqual(lexem.read(), 'ijkl')

    def test_raise_error(self) -> None:
        """ force production calling that not exists """
        parser = CrupyParserBase({
            'entry'  : CrupyLexerOpProductionCall('entry2'),
        })
        self.assertRaises(
            exc_obj     = CrupyParserException(
                'Unable to find the primary production entry name '
                '\'entry2\''
            ),
            request     = (parser, 'execute', 'entry', '\tabcdef ijkl'),
        )
