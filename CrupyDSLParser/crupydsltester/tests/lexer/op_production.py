"""
tests.lexer.op_production   - test the CrupyLexerOpProduction
"""
__all__ = (
    'CrupyUnittestLexerProd',
)

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.parser import CrupyParserBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpProductionCall,
    CrupyLexerOpText,
    CrupyLexerOpProductionCallException,
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
            cls_exc = CrupyLexerOpProductionCallException,
            request = (parser, 'execute', 'entry'),
            error   = \
                'Stream: line 1, column 1\n'
                'abcdefijkl\n'
                '^\n'
                'CrupyLexerOpProductionCallException: Unable to find the '
                'production named \'entry2\''
        )
        try:
            parser.execute('entry')
            self.assertAlways('production entry has been executed')
        except CrupyLexerOpProductionCallException as err:
            self.assertEqual(err.production, 'entry2')
            self.assertEqual(
                err.reason,
                'unable to find the production named \'entry2\''
            )
