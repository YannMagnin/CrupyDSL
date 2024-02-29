"""
tests.stream.stream     - stream object unittest
"""
__all__ = [
    'CrupyUnittestStream',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._stream import CrupyStream

#---
# Public
#---

class CrupyUnittestStream(CrupyUnittestBase):
    """ unittest suit for the crypu stream object
    """

    #---
    # Public tests
    #---

    def test_read_peek(self) -> None:
        """ simply check the read/peek
        """
        stream = CrupyStream.from_any('abcd')
        for ctest in 'abcd':
            self.assertEqual(stream.peek_char(), ctest)
            self.assertEqual(stream.read_char(), ctest)
        self.assertIsNone(stream.peek_char())
        self.assertIsNone(stream.read_char())

    def test_context(self) -> None:
        """ check context handling
        """
        stream = CrupyStream.from_any('abcdef')
        with stream as lexem:
            self.assertEqual(lexem.read_char(), 'a')
            self.assertEqual(lexem.read_char(), 'b')
            with stream as lexem2:
                self.assertEqual(lexem2.read_char(), 'c')
                lexem2.validate()
            self.assertEqual(lexem.read_char(), 'd')
        with stream as lexem:
            self.assertEqual(lexem.read_char(), 'a')
            self.assertEqual(lexem.read_char(), 'b')
            with stream as lexem2:
                self.assertEqual(lexem2.read_char(), 'c')
                with stream as lexem3:
                    self.assertEqual(lexem3.read_char(), 'd')
                    lexem3.validate()
                self.assertEqual(lexem2.read_char(), 'e')
            self.assertEqual(lexem.read_char(), 'c')
