"""
tests.lexer.op_production   - test the CrupyLexerOpProduction
"""
__all__ = (
    'CrupyUnittestLexerProd',
)

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core.parser import CrupyParserBase
from crupydslparser.core._lexer import (
    CrupyLexerOpProductionCall,
    CrupyLexerOpText,
    CrupyLexerException,
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
        parser.register_stream('abcdefijkl')
        test = parser.execute('entry')
        self.assertEqual(test.text, 'abcdef')
        with parser.stream as context:
            for n in 'ijkl':
                self.assertEqual(context.read_char(), n)

    def test_raise_error(self) -> None:
        """ force production calling that not exists """
        parser = CrupyParserBase({
            'entry'  : CrupyLexerOpProductionCall('entry2'),
        })
        parser.register_stream('abcdefijkl')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 1\n'
                'abcdefijkl\n'
                '^\n'
                'CrupyLexerOpProductionCall: Unable to find the '
                'production named \'entry2\''
            ),
            (parser, 'execute', 'entry'),
        )
