"""
crupydsl._dsl._parser.string  - handle string production
"""
__all__ = [
    'CrupyDSLParserNodeDslString',
    'dsl_string_hook',
    'dsl_string_hook_error'
]
from crupydsl.parser.node import CrupyDSLParserNodeBase
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.grammar._dsl._parser.exception import (
    CrupyDSLParserException,
)

#---
# Public
#---

class CrupyDSLParserNodeDslString(CrupyDSLParserNodeBase):
    """ DSL "string" node """
    text:   str

def dsl_string_hook(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
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
    return CrupyDSLParserNodeDslString(
        parent_node = node,
        text        = text,
    )

def dsl_string_hook_error(
    err: CrupyDSLParserBaseException,
) -> CrupyDSLParserBaseException:
    """ string error hook
    """
    assert err.type == 'lexer_op_or'
    err = err.deepest_error
    assert err.type == 'lexer_op_seq'
    if err.validated_operation == 0:
        return CrupyDSLParserException(err, 'missing starting quote')
    if err.validated_operation == 1:
        return CrupyDSLParserException(
            err,
            'unable to capture string content',
        )
    if err.validated_operation == 2:
        return CrupyDSLParserException(err, 'missing enclosing quote')
    return CrupyDSLParserException(
        err,
        '[internal error] unsupported sequence, too many validated '
        f"operation ({err.validated_operation} > 2)"
    )
