"""
tests.lexer.op_rep  - tes for the CrupyLexerRep0N, and CrupyLexerRep1N
"""
__all__ = [
    'CrupyUnittestLexerRep',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._stream import CrupyStream
from crupydslparser.core._lexer import (
    CrupyLexerText,
    CrupyLexerRep0N,
    CrupyLexerRep1N,
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
        stream = CrupyStream.from_any('abcdef ij abc def ijklnm')
        reptok = CrupyLexerRep0N(
            CrupyLexerText('abc'),
            CrupyLexerText('def'),
            CrupyLexerText('ij'),
        )(stream)
        self.assertIsNotNone(reptok)
        if reptok is None:
            return
        self.assertIsNotNone(reptok['rep'])
        self.assertEqual(len(reptok['rep']), 2)
        self.assertEqual(len(reptok['rep'][0]), 3)
        self.assertEqual(reptok['rep'][0][0]['text'], 'abc')
        self.assertEqual(reptok['rep'][0][1]['text'], 'def')
        self.assertEqual(reptok['rep'][0][2]['text'], 'ij')
        self.assertEqual(reptok['rep'][1][0]['text'], 'abc')
        self.assertEqual(reptok['rep'][1][1]['text'], 'def')
        self.assertEqual(reptok['rep'][1][2]['text'], 'ij')

    def test_rep0n_empty(self) -> None:
        """ simple empty """
        stream = CrupyStream.from_any('  abcdef ij abc def ijklnm')
        reptok = CrupyLexerRep0N(
            CrupyLexerText('zzz'),
            CrupyLexerText('def'),
            CrupyLexerText('ijk'),
        )(stream)
        self.assertIsNotNone(reptok)
        if reptok is None:
            return
        self.assertIsNotNone(reptok['rep'])
        self.assertEqual(len(reptok['rep']), 0)

    ## Rep1N

    def test_rep1n_simple_success(self) -> None:
        """ simple valid case """
        stream = CrupyStream.from_any('abcdef ij')
        reptok = CrupyLexerRep1N(
            CrupyLexerText('abc'),
            CrupyLexerText('def'),
            CrupyLexerText('ij'),
        )(stream)
        self.assertIsNotNone(reptok)
        if reptok is None:
            return
        self.assertIsNotNone(reptok['rep'])
        self.assertEqual(len(reptok['rep']), 1)
        self.assertEqual(len(reptok['rep'][0]), 3)
        self.assertEqual(reptok['rep'][0][0]['text'], 'abc')
        self.assertEqual(reptok['rep'][0][1]['text'], 'def')
        self.assertEqual(reptok['rep'][0][2]['text'], 'ij')

    def test_rep1n_empty(self) -> None:
        """ simple empty """
        stream = CrupyStream.from_any('  abcdef ij abc def ijklnm')
        reptok = CrupyLexerRep1N(
            CrupyLexerText('zzz'),
            CrupyLexerText('def'),
            CrupyLexerText('ijk'),
        )(stream)
        self.assertIsNone(reptok)
