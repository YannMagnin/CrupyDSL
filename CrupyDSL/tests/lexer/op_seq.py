"""
tests.lexer.op_seq  - test the CrupyDSLLexerOpSeq
"""
from crupydsl.parser import CrupyDSLParserBase
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpSeq,
    CrupyDSLLexerOpSeqException,
    CrupyDSLLexerOpText,
)

#---
# Public
#---

def test_simple_success() -> None:
    """ simple valid case
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpText('abc'),
            CrupyDSLLexerOpText('def'),
            CrupyDSLLexerOpText('ij'),
        ),
    })
    parser.register_stream('abcdefijkl')
    seqtok = parser.execute('entry')
    assert seqtok.seq is not None
    assert len(seqtok.seq) == 3
    assert seqtok.seq[0].text == 'abc'
    assert seqtok.seq[1].text == 'def'
    assert seqtok.seq[2].text == 'ij'
    with parser.stream as context:
        assert context.read_char() == 'k'
        assert context.read_char() == 'l'
        context.validate()

def test_simple_fail() -> None:
    """ simple fail
    """
    parser = CrupyDSLParserBase({
        'entry' : CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpText('abc'),
            CrupyDSLLexerOpText('dex'),
            CrupyDSLLexerOpText('ijkl'),
        ),
    })
    try:
        parser.register_stream('abcdef ijkl')
        parser.execute('entry')
        raise AssertionError('rule entry executed')
    except CrupyDSLLexerOpSeqException as err:
        assert str(err) == (
            'Lexer parsing error occured:\n'
            '\n'
            'Stream: line 1, column 6\n'
            'abcdef ijkl\n'
            '   ~~^\n'
            'CrupyDSLLexerOpTextException: Unable to match the text \'dex\''
        )
        assert err.validated_operation == 1
        assert err.reason == 'unable to match the text \'dex\''
    with parser.stream as context:
        for n in 'abcdef ijkl':
            assert context.read_char() == n
