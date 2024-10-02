"""
crupydsl.grammar._dsl._parser.group  - DSL group hook
"""
__all__ = [
    'CrupyDSLParserNodeDslGroup',
    'dsl_group_hook',
    'dsl_group_hook_error',
]
from typing import Union, NoReturn

from crupydsl.parser import CrupyDSLParserNodeBase
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.grammar._dsl._parser.exception import (
    CrupyDSLParserException,
)

#---
# Public
#---

class CrupyDSLParserNodeDslGroup(CrupyDSLParserNodeBase):
    """ group node """
    lookahead:  Union[str,None]
    statement:  CrupyDSLParserNodeBase
    operation:  Union[str,None]

def dsl_group_hook(node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
    """ handle "group" node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 7
    assert node.seq[0].type == 'lex_text'
    assert node.seq[1].type == 'lex_optional'
    assert node.seq[2].type == 'dsl_space'
    assert node.seq[3].type == 'dsl_statement'
    assert node.seq[4].type == 'dsl_space'
    assert node.seq[5].type == 'lex_text'
    assert node.seq[6].type == 'lex_optional'
    lookahead: Union[str,None] = None
    if node.seq[1].seq:
        assert len(node.seq[1].seq) == 2
        assert node.seq[1].seq[0].type == 'lex_text'
        assert node.seq[1].seq[0].text == '?'
        assert node.seq[1].seq[1].type == 'lex_text'
        assert node.seq[1].seq[1].text in '!='
        lookahead = 'negative'
        if node.seq[1].seq[1].text == '=':
            lookahead = 'positive'
    operation: Union[str,None] = None
    if node.seq[6].seq:
        assert len(node.seq[6].seq) == 1
        assert node.seq[6].seq[0].type == 'lex_text'
        assert node.seq[6].seq[0].text in '*+?'
        operation = 'zero_plus'
        if node.seq[6].seq[0].text == '+':
            operation = 'one_plus'
        if node.seq[6].seq[0].text == '?':
            operation = 'optional'
    return CrupyDSLParserNodeDslGroup(
        parent_node = node,
        lookahead   = lookahead,
        statement   = node.seq[3],
        operation   = operation,
    )

def dsl_group_hook_error(err: CrupyDSLParserBaseException) -> NoReturn:
    """ error hook
    """
    assert err.type == 'lexer_op_seq'
    if err.validated_operation == 0:
        raise CrupyDSLParserException(err, 'missing opening parenthesis')
    if err.validated_operation in (2, 3, 4):
        raise err
    if err.validated_operation == 5:
        raise CrupyDSLParserException(err, 'missing enclosing parenthesis')
    raise CrupyDSLParserException(
        err,
        '[internal error] unsupported sequence, too many validated '
        f"operation ({err.validated_operation} > 2)"
    )
