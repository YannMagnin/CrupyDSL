"""
crupydslparser._dsl._parser.string  - handle string production
"""
__all__ = [
    'CrupyParserNodeDslString',
    'dsl_string_hook',
    'dsl_string_hook_error'
]
from typing import NoReturn

from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser.parser.exception import CrupyParserBaseException
from crupydslparser.grammar._dsl._parser.exception import (
    CrupyDslParserException,
)

#---
# Public
#---

class CrupyParserNodeDslString(CrupyParserNodeBase):
    """ DSL "string" node """
    text:   str

def dsl_string_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle `string` node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'lex_text'
    assert node.seq[1].type == 'lex_rep'
    assert node.seq[2].type == 'lex_text'
    assert node.seq[0].text in '\'"'
    assert node.seq[2].text in '\'"'
    assert node.seq[0].text == node.seq[2].text
    text = ''
    for seq in node.seq[1].rep:
        assert len(seq) == 1
        assert seq[0].type == 'lex_text'
        text += seq[0].text
    return CrupyParserNodeDslString(
        parent_node = node,
        text        = text,
    )

def dsl_string_hook_error(err: CrupyParserBaseException) -> NoReturn:
    """ string error hook
    """
    assert err.type == 'lexer_op_or'
    err = err.deepest_error
    assert err.type == 'lexer_op_seq'
    if err.validated_operation == 0:
        raise CrupyDslParserException(err, 'missing starting quote')
    if err.validated_operation == 1:
        raise CrupyDslParserException(
            err,
            'unable to capture string content',
        )
    if err.validated_operation == 2:
        raise CrupyDslParserException(err, 'missing enclosing quote')
    raise CrupyDslParserException(
        err,
        '[internal error] unsupported sequence, too many validated '
        f"operation ({err.validated_operation} > 2)"
    )
