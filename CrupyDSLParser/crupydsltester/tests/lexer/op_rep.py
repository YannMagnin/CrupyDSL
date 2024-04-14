"""
tests.lexer.op_rep  - tes for the CrupyLexerOpRep0N, and CrupyLexerOpRep1N
"""
__all__ = (
    'CrupyUnittestLexerRep',
)

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.parser import CrupyParserBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpText,
    CrupyLexerOpRep0N,
    CrupyLexerOpRep1N,
    CrupyLexerException,
)

#---
# Public
#---

class CrupyUnittestLexerRep(CrupyUnittestBase):
    """ unittest suite for the crupy lexer sequence operation
    """

    #---
    # Public tests
    #---

    ## Rep0N

    def test_rep0n_simple_success(self) -> None:
        """ simple valid case """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpRep0N(
                CrupyLexerOpText('abc'),
                CrupyLexerOpText('def'),
                CrupyLexerOpText('ij'),
            ),
        })
        parser.register_stream('abcdefijabcdefijklnm')
        reptok = parser.execute('entry')
        self.assertIsNotNone(reptok.rep)
        self.assertEqual(len(reptok.rep), 2)
        self.assertEqual(len(reptok.rep[0]), 3)
        self.assertEqual(reptok.rep[0][0].text, 'abc')
        self.assertEqual(reptok.rep[0][1].text, 'def')
        self.assertEqual(reptok.rep[0][2].text, 'ij')
        self.assertEqual(reptok.rep[1][0].text, 'abc')
        self.assertEqual(reptok.rep[1][1].text, 'def')
        self.assertEqual(reptok.rep[1][2].text, 'ij')

    def test_rep0n_empty(self) -> None:
        """ simple empty """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpRep0N(
                CrupyLexerOpText('zzz'),
                CrupyLexerOpText('def'),
                CrupyLexerOpText('ijk'),
            ),
        })
        parser.register_stream('abcdefijabcdefijklnm')
        reptok = parser.execute('entry')
        self.assertIsNotNone(reptok.rep)
        self.assertEqual(len(reptok.rep), 0)

    ## Rep1N

    def test_rep1n_simple_success(self) -> None:
        """ simple valid case """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpRep1N(
                CrupyLexerOpText('abc'),
                CrupyLexerOpText('def'),
                CrupyLexerOpText('ij'),
            ),
        })
        parser.register_stream('abcdefij')
        reptok = parser.execute('entry')
        self.assertIsNotNone(reptok.rep)
        self.assertEqual(len(reptok.rep), 1)
        self.assertEqual(len(reptok.rep[0]), 3)
        self.assertEqual(reptok.rep[0][0].text, 'abc')
        self.assertEqual(reptok.rep[0][1].text, 'def')
        self.assertEqual(reptok.rep[0][2].text, 'ij')

    def test_rep1n_empty(self) -> None:
        """ simple empty """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpRep1N(
                CrupyLexerOpText('abc'),
                CrupyLexerOpText('def'),
                CrupyLexerOpText('ijk'),
            ),
        })
        parser.register_stream('abcdefijabcdefijklnm')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 9\n'
                'abcdefijabcdefijklnm\n'
                '~~~~~~~~^\n'
                'CrupyLexerOpRep1N: Unable to perform at least one '
                'repetition of the sequence. Reason:\n'
                'CrupyLexerOpRep1N: Unable to validate the operation number 3'
            ),
            (parser, 'execute', 'entry'),
        )