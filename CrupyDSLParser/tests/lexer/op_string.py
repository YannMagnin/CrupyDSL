"""
tests.lexer.op_text     - test the CrupyLexerText
"""
__all__ = [
    'CrupyUnittestLexerText',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core.parser._base import CrupyParserBase
from crupydslparser.core._lexer import CrupyLexerText

#---
# Public
#---

class CrupyUnittestLexerText(CrupyUnittestBase):
    """ unittest suite for the crupy lexer text operation
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid cases """
        parser = CrupyParserBase({
            'entry0' : CrupyLexerText('abcdef'),
            'entry1' : CrupyLexerText('i'),
            'entry2' : CrupyLexerText('jkc'),
            'entry3' : CrupyLexerText('jkl'),
        })
        strop0 = parser.execute('entry0', 'abcdef ijkl')
        strop1 = parser.execute('entry1')
        strop2 = parser.execute('entry2')
        strop3 = parser.execute('entry3')
        self.assertIsNotNone(strop0)
        self.assertIsNotNone(strop1)
        self.assertIsNone(strop2)
        self.assertIsNotNone(strop3)
