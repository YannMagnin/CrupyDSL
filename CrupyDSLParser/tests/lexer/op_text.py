"""
tests.lexer.op_text     - test the CrupyLexerOpText
"""
__all__ = [
    'CrupyUnittestLexerText',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core.parser import CrupyParserBase
from crupydslparser.core._lexer import CrupyLexerOpText

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
            'entry0' : CrupyLexerOpText('abcdef'),
            'entry1' : CrupyLexerOpText('i'),
            'entry2' : CrupyLexerOpText('jkc'),
            'entry3' : CrupyLexerOpText('jkl'),
        })
        parser.register_stream('abcdefijkl')
        strop0 = parser.execute('entry0')
        strop1 = parser.execute('entry1')
        strop2 = parser.execute('entry2')
        strop3 = parser.execute('entry3')
        self.assertIsNotNone(strop0)
        self.assertIsNotNone(strop1)
        self.assertIsNone(strop2)
        self.assertIsNotNone(strop3)
