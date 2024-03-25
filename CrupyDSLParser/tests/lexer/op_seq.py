"""
tests.lexer.op_seq  - test the CrupyLexerOpSeq
"""
__all__ = [
    'CrupyUnittestLexerSeq',
]

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
        seqtok = parser.execute('entry', False)
        self.assertIsNotNone(seqtok)
        if seqtok is None:
            return
        self.assertIsNotNone(seqtok.seq)
        self.assertEqual(len(seqtok.seq), 3)
        self.assertEqual(seqtok.seq[0].text, 'abc')
        self.assertEqual(seqtok.seq[1].text, 'def')
        self.assertEqual(seqtok.seq[2].text, 'ij')
        with parser.stream as lexem:
            self.assertEqual(lexem.read(), 'kl')
            lexem.validate()

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
        seqtok = parser.execute('entry', False)
        self.assertIsNone(seqtok)

    def test_retrograde_fail(self) -> None:
        """ partial valid sequence """
        parser = CrupyParserBase({
            'entry' : CrupyLexerOpSeq(
                CrupyLexerOpText('abc'),
                CrupyLexerOpText('def'),
                CrupyLexerOpText('ijxl'),
            ),
        })
        parser.register_stream('abcdefijkl')
        seqtok = parser.execute('entry', False)
        self.assertIsNone(seqtok)
        with parser.stream as lexem:
            self.assertEqual(lexem.read(), 'abcdefijkl')

    def test_simple_error(self) -> None:
        """ simple error """
        parser = CrupyParserBase({
            'entry' : \
                CrupyLexerOpSeq(
                    CrupyLexerOpText('abcdef'),
                    CrupyLexerOpText('zz'),
                ),
        })
        parser.register_stream('abcdefghij')
        self.assertRaises(
            CrupyLexerException(
                'Parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 7\n'
                'abcdefghij\n'
                '      ^\n'
                '\n'
                'SyntaxError: invalid syntax (unable to find '
                'appropriate production to parse this stream here)'
            ),
            (parser, 'execute', 'entry', True),
        )
