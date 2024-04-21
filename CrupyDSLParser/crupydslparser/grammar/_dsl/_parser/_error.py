"""
crupydslparser.grammar._dsl._parser.error  - DSL error hook
"""
__all__ = [
    'dsl_error_hook',
    'dsl_error_hook_error',
]
from typing import NoReturn

from crupydslparser.parser import CrupyParserNodeBase
from crupydslparser.parser.exception import CrupyParserBaseException
from crupydslparser.grammar._dsl._parser.exception import (
    CrupyDslParserException,
)

#---
# Public
#---

class CrupyParserNodeDslError(CrupyParserNodeBase):
    """ error node """
    error_name: str
    kind: str

def dsl_error_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle "error" node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 5
    assert node.seq[0].type == 'lex_text'
    assert node.seq[0].text == '@'
    assert node.seq[1].type == 'lex_text'
    assert node.seq[1].text in ('error', 'error_hook')
    assert node.seq[2].type == 'lex_text'
    assert node.seq[2].text == '('
    assert node.seq[3].type == 'dsl_string'
    assert node.seq[4].type == 'lex_text'
    assert node.seq[4].text == ')'
    return CrupyParserNodeDslError(
        parent_node = node,
        error_name  = node.seq[3].text,
        kind        = 'error' if node.seq[1].text == 'error' else 'hook',
    )

def dsl_error_hook_error(err: CrupyParserBaseException) -> NoReturn:
    """ string error hook
    """
    assert err.type == 'lexer_op_seq'
    if err.validated_operation == 0:
        raise CrupyDslParserException(
            err,
            'manual error must start with "@"',
        )
    if err.validated_operation == 1:
        raise CrupyDslParserException(
            err,
            'only \'error\' and \'error_hook\' are currently supported',
        )
    if err.validated_operation == 2:
        raise CrupyDslParserException(err, 'missing opening parenthesis')
    if err.validated_operation == 3:
        raise err
    if err.validated_operation == 4:
        raise CrupyDslParserException(err, 'missing enclosing parenthesis')
    raise CrupyDslParserException(
        err,
        '[internal error] unsupported sequence '
        f"({err.validated_operation})"
    )
