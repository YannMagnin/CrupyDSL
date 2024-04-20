"""
tests.lexer.op_seq  - test the CrupyLexerOpSeq
"""
__all__ = (
    'CrupyUnittestLexerSeq',
)

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.parser import CrupyParserBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpSeq,
    CrupyLexerOpSeqException,
    CrupyLexerOpText,
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
            cls_exc = CrupyLexerOpSeqException,
            request = (parser, 'execute', 'entry'),
            error   = \
                'Lexer parsing error occured:\n'
                '\n'
                'Stream: line 1, column 6\n'
                'abcdef ijkl\n'
                '~~~~~^\n'
                'CrupyLexerOpSeqException: Unable to validate the '
                'operation number 2'
        )
        try:
            parser.execute('entry')
            self.assertAlways('production entry has been executed')
        except CrupyLexerOpSeqException as err:
            self.assertEqual(err.validated_operation, 1)
            self.assertEqual(
                err.reason,
                'unable to validate the operation number 2',
            )
        with parser.stream as context:
            for n in 'abcdef ijkl':
                self.assertEqual(context.read_char(), n)
