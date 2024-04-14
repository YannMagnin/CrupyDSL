"""
tests.stream.stream     - stream object unittest
"""
__all__ = (
    'CrupyUnittestStream',
)

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.parser._stream.stream import CrupyStream

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
                '~~^'
            )

    def test_error_context_multiline(self) -> None:
        """ check context error generation in multiline
        """
        stream = CrupyStream.from_any('abc\noui')
        with stream as context:
            self.assertEqual(context.read_char(), 'a')
            self.assertEqual(context.read_char(), 'b')
            context.validate()
        with stream as context:
            self.assertEqual(context.read_char(), 'c')
            self.assertEqual(context.read_char(), '\n')
            self.assertEqual(context.read_char(), 'o')
            self.assertEqual(
                context.generate_error_log(),
                'Stream: line 2, column 2\n'
                'oui\n'
                '~^'
            )

    def test_error_context_longline(self) -> None:
        """ check context error generation in longline
        """
        stream = CrupyStream.from_any('abc oui')
        with stream as context:
            self.assertEqual(context.read_char(), 'a')
            self.assertEqual(context.read_char(), 'b')
            self.assertEqual(context.read_char(), 'c')
            self.assertEqual(context.read_char(), ' ')
            context.validate()
        with stream as context:
            self.assertEqual(context.read_char(), 'o')
            self.assertEqual(context.read_char(), 'u')
            self.assertEqual(
                context.generate_error_log(),
                'Stream: line 1, column 7\n'
                'abc oui\n'
                '    ~~^'
            )
