"""
tests.lexer.op_seq  - test the CrupyLexerSeq
"""
__all__ = [
    'CrupyUnittestLexerSeq',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._lexer import CrupyLexerSeq, CrupyLexerText
from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyUnittestLexerSeq(CrupyUnittestBase):
    """ unittest suite for the crupy lexer sequence operation
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid case """
        stream = CrupyStream.from_any('abcdef ijkl')
        seqtok = CrupyLexerSeq(
            CrupyLexerText('abc'),
            CrupyLexerText('def'),
            CrupyLexerText('ij'),
        )(stream)
        self.assertIsNotNone(seqtok)
        if seqtok is None:
            return
        self.assertIsNotNone(seqtok['seq'])
        self.assertEqual(len(seqtok['seq']), 3)
        self.assertEqual(seqtok['seq'][0]['text'], 'abc')
        self.assertEqual(seqtok['seq'][1]['text'], 'def')
        self.assertEqual(seqtok['seq'][2]['text'], 'ij')
        with stream as lexem:
            self.assertEqual(lexem.read(), 'kl')
            lexem.validate()

    def test_simple_fail(self) -> None:
        """ simple fail """
        stream = CrupyStream.from_any('abcdef ijkl')
        seqtok = CrupyLexerSeq(
            CrupyLexerText('abc'),
            CrupyLexerText('dex'),
            CrupyLexerText('ijkl'),
        )(stream)
        self.assertIsNone(seqtok)

    def test_retrograde_fail(self) -> None:
        """ partial valid sequence """
        stream = CrupyStream.from_any('abcdef ijkl')
        seqtok = CrupyLexerSeq(
            CrupyLexerText('abc'),
            CrupyLexerText('def'),
            CrupyLexerText('ijxl'),
        )(stream)
        self.assertIsNone(seqtok)
        with stream as lexem:
            self.assertEqual(lexem.read(), 'abcdef')
