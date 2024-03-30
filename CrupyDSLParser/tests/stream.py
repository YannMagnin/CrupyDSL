"""
tests.stream.stream     - stream object unittest
"""
__all__ = (
    'CrupyUnittestStream',
)

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
        with stream as context:
            for ctest in 'abcd':
                self.assertEqual(context.peek_char(), ctest)
                self.assertEqual(context.read_char(), ctest)
            self.assertIsNone(context.peek_char())
            self.assertIsNone(context.read_char())

    def test_context(self) -> None:
        """ check context handling
        """
        stream = CrupyStream.from_any('abcdef')
        with stream as context:
            self.assertEqual(context.read_char(), 'a')
            self.assertEqual(context.read_char(), 'b')
            with stream as context2:
                self.assertEqual(context2.read_char(), 'c')
                context2.validate()
            self.assertEqual(context.read_char(), 'd')
        with stream as context:
            self.assertEqual(context.read_char(), 'a')
            self.assertEqual(context.read_char(), 'b')
            with stream as context2:
                self.assertEqual(context2.read_char(), 'c')
                with stream as context3:
                    self.assertEqual(context3.read_char(), 'd')
                    context3.validate()
                self.assertEqual(context2.read_char(), 'e')
            self.assertEqual(context.read_char(), 'c')

    def test_error_context(self) -> None:
        """ check context error generation """
        stream = CrupyStream.from_any('abcdef\noui')
        with stream as context:
            self.assertEqual(context.read_char(), 'a')
            self.assertEqual(context.read_char(), 'b')
            self.assertEqual(
                context.generate_error_log(),
                'Stream: line 1, column 3\n'
                'abcdef\n'
                '  ^'
            )
