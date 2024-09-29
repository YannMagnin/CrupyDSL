"""
tests.stream.stream     - stream object unittest
"""
from crupydslparser.parser._stream.stream import CrupyStream

#---
# Public
#---

def test_read_peek() -> None:
    """ simply check the read/peek
    """
    stream = CrupyStream.from_any('abcd\n\r\r\n0')
    with stream as context:
        for ctest in 'abcd\n\r':
            assert context.peek_char() == ctest
            assert context.read_char() == ctest
        assert context.peek_char() == '\r\n'
        assert context.read_char() == '\r\n'
        assert context.peek_char() == '0'
        assert context.read_char() == '0'
        assert context.peek_char() is None
        assert context.read_char() is None

def test_context() -> None:
    """ check context handling
    """
    stream = CrupyStream.from_any('abcdef')
    with stream as context:
        assert context.read_char() == 'a'
        assert context.read_char() == 'b'
        with stream as context2:
            assert context2.read_char() == 'c'
            context2.validate()
        assert context.read_char() == 'd'
    with stream as context:
        assert context.read_char() == 'a'
        assert context.read_char() == 'b'
        with stream as context2:
            assert context2.read_char() == 'c'
            with stream as context3:
                assert context3.read_char() == 'd'
                context3.validate()
            assert context2.read_char() == 'e'
        assert context.read_char() == 'c'

def test_error_context() -> None:
    """ check context error generation
    """
    stream = CrupyStream.from_any('abcdef\noui')
    with stream as context:
        assert context.read_char() == 'a'
        assert context.read_char() == 'b'
        assert context.generate_error_log() == (
            'Stream: line 1, column 3\n'
            'abcdef\\n\n'
            '~~^'
        )

def test_error_context_multiline_0() -> None:
    """ check context error generation in multiline
    """
    stream = CrupyStream.from_any('abc\noui\r\nnon foo bar')
    with stream as context:
        assert context.read_char() == 'a'
        assert context.read_char() == 'b'
        context.validate()
    with stream as context:
        assert context.read_char() == 'c'
        assert context.read_char() == '\n'
        assert context.read_char() == 'o'
        assert context.generate_error_log() == (
            'Stream: line 2, column 2\n'
            'oui\\r\\n\n'
            '~^'
        )
        assert context.read_char() == 'u'
        assert context.read_char() == 'i'
        assert context.read_char() == '\r\n'
        assert context.generate_error_log() == (
            'Stream: line 3, column 1\n'
            'non foo bar\n'
            '^'
        )

def test_error_context_multiline_1() -> None:
    """ check context error generation in multiline
    """
    stream = CrupyStream.from_any('abc\noui\r\nnon foo bar')
    with stream as context:
        assert context.read_char() == 'a'
        assert context.read_char() == 'b'
        assert context.read_char() == 'c'
        assert context.read_char() == '\n'
        context.validate()
    with stream as context:
        assert context.read_char() == 'o'
        assert context.read_char() == 'u'
        assert context.read_char() == 'i'
        assert context.generate_error_log() == (
            'Stream: line 2, column 4\n'
            'oui\\r\\n\n'
            '~~~^'
        )

def test_error_context_longline() -> None:
    """ check context error generation in longline
    """
    stream = CrupyStream.from_any('abc oui')
    with stream as context:
        assert context.read_char() == 'a'
        assert context.read_char() == 'b'
        assert context.read_char() == 'c'
        assert context.read_char() == ' '
        context.validate()
    with stream as context:
        assert context.read_char() == 'o'
        assert context.read_char() == 'u'
        assert context.generate_error_log() == (
            'Stream: line 1, column 7\n'
            'abc oui\n'
            '    ~~^'
        )
