"""
tests.lexer.op_seq  - test the CrupyLexerOpSeq
"""
__all__ = (
    'CrupyUnittestLexerSeq',
)

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core.parser import CrupyParserBase
from crupydslparser.core._lexer import (
    CrupyLexerOpSeq,
    CrupyLexerOpText,
    CrupyLexerException,
)

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
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpSeq(
                CrupyLexerOpText('abc'),
                CrupyLexerOpText('def'),
                CrupyLexerOpText('ij'),
            ),
        })
        parser.register_stream('abcdefijkl')
        seqtok = parser.execute('entry')
        self.assertIsNotNone(seqtok)
        if seqtok is None:
            return
        self.assertIsNotNone(seqtok.seq)
        self.assertEqual(len(seqtok.seq), 3)
        self.assertEqual(seqtok.seq[0].text, 'abc')
        self.assertEqual(seqtok.seq[1].text, 'def')
        self.assertEqual(seqtok.seq[2].text, 'ij')
        with parser.stream as context:
            self.assertEqual(context.read_char(), 'k')
            self.assertEqual(context.read_char(), 'l')
            context.validate()

    def test_simple_fail(self) -> None:
        """ simple fail """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpSeq(
                CrupyLexerOpText('abc'),
                CrupyLexerOpText('dex'),
                CrupyLexerOpText('ijkl'),
            ),
        })
        parser.register_stream('abcdef ijkl')
        self.assertRaises(
            CrupyLexerException(
                'Stream: line 1, column 6\n'
                'abcdef ijkl\n'
                '~~~~~^\n'
                'CrupyLexerOpSeq: Unable to validate the operation number 2'
            ),
            (parser, 'execute', 'entry'),
        )
        with parser.stream as context:
            for n in 'abcdef ijkl':
                self.assertEqual(context.read_char(), n)
