"""
crupydsl.grammar._dsl._parser.between     - DSL between hook
"""
__all__ = [
    'CrupyDSLParserNodeDslBetween',
    'dsl_between_hook',
    'dsl_between_hook_error',
]
from crupydsl.parser import (
    CrupyDSLParserNodeBase,
    CrupyDSLParserBaseException,
)
from crupydsl.grammar._dsl._parser.exception import (
    CrupyDSLParserException,
)

#---
# Public
#---

class CrupyDSLParserNodeDslBetween(CrupyDSLParserNodeBase):
    """ builtin node
    """
    kind:   str
    opening: CrupyDSLParserNodeBase
    closing: CrupyDSLParserNodeBase

def dsl_between_hook(node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
    """ between node hook
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[1].type == 'lex_text'
    assert node.seq[1].text in ('...', '.!.')
    return CrupyDSLParserNodeDslBetween(
        parent_node = node,
        kind    = 'no_newline' if node.seq[1].text == '...' else 'newline',
        opening = node.seq[0],
        closing = node.seq[2],
    )

def dsl_between_hook_error(
    err: CrupyDSLParserBaseException,
) -> CrupyDSLParserBaseException:
    """ error hook
    """
    assert getattr(err, 'validated_operation', None) is not None
    if err.validated_operation == 0:
        return CrupyDSLParserException(
            error   = err,
            reason  = 'unable to validate the opening request',
        )
    if err.validated_operation == 1:
        return CrupyDSLParserException(
            error   = err,
            reason  = \
                'unable to validate the type of between operation '
                'requested',
        )
    return CrupyDSLParserException(
        error   = err,
        reason  = 'unable to validate the enclosing request',
    )
