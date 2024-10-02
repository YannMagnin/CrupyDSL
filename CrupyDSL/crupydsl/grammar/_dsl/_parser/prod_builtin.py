"""
crupydsl.grammar._dsl._parser.builtin  - DSL builtin hook
"""
__all__ = [
    'CrupyDSLParserNodeDslBuiltin',
    'dsl_builtin_hook',
    'dsl_builtin_hook_error',
]
from typing import NoReturn

from crupydsl.parser import CrupyDSLParserNodeBase
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.grammar._dsl._parser.exception import (
    CrupyDSLParserException,
)

#---
# Public
#---

class CrupyDSLParserNodeDslBuiltin(CrupyDSLParserNodeBase):
    """ builtin node
    """
    kind:   str

def dsl_builtin_hook(node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
    """ handle "builtin" node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'lex_text'
    assert node.seq[0].text == ':'
    assert node.seq[2].type == 'lex_text'
    assert node.seq[2].text == ':'
    assert node.seq[1].type == 'lex_rep'
    kind = ''
    for text in node.seq[1].rep:
        assert len(text) == 1
        assert text[0].type == 'lex_text'
        kind += text[0].text
    return CrupyDSLParserNodeDslBuiltin(
        parent_node = node,
        kind        = kind,
    )

def dsl_builtin_hook_error(err: CrupyDSLParserBaseException) -> NoReturn:
    """ builtin error hook
    """
    assert err.type == 'lexer_op_seq'
    if err.validated_operation == 0:
        raise CrupyDSLParserException(err, 'missing starting colon')
    if err.validated_operation == 1:
        raise CrupyDSLParserException(err, 'missing builtin name')
    if err.validated_operation == 2:
        raise CrupyDSLParserException(err, 'missing enclosing colon')
    raise CrupyDSLParserException(
        err,
        '[internal error] unsupported sequence, too many validated '
        f"operation ({err.validated_operation} > 2)"
    )
