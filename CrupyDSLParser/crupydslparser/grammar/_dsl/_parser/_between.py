"""
crupydslparser.grammar._dsl._parser.between     - DSL between hook
"""
__all__ = [
    'dsl_between_hook',
    'dsl_between_hook_error',
]
from typing import NoReturn

from crupydslparser.parser import (
    CrupyParserNodeBase,
    CrupyParserBaseException,
)
from crupydslparser.grammar._dsl._parser.exception import (
    CrupyDslParserException,
)

#---
# Public
#---

class CrupyParserNodeDslBetween(CrupyParserNodeBase):
    """ builtin node
    """
    kind:   str
    opening: CrupyParserNodeBase
    closing: CrupyParserNodeBase

def dsl_between_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ between node hook
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[1].type == 'lex_text'
    return CrupyParserNodeDslBetween(
        parent_node = node,
        kind    = 'no_newline' if node.seq[1].text == '...' else 'newline',
        opening = node.seq[0],
        closing = node.seq[2],
    )

def dsl_between_hook_error(
    err: CrupyParserBaseException,
) -> NoReturn:
    """ error hook
    """
    assert getattr(err, 'validated_operation', None) is not None
    if err.validated_operation == 0:
        raise CrupyDslParserException(
            error   = err,
            reason  = 'unable to validate the opening request',
        )
    if err.validated_operation == 1:
        raise CrupyDslParserException(
            error   = err,
            reason  = \
                'unable to validate the type of between operation '
                'requested',
        )
    raise CrupyDslParserException(
        error   = err,
        reason  = 'unable to validate the enclosing request',
    )
