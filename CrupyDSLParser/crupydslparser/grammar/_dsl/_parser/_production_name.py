"""
crupydslparser.grammar._dsl._parser.production_name  - DSL parser hook
"""
__all__ = [
    'CrupyParserNodeDslProductionName',
    'dsl_production_name_hook',
    'dsl_production_name_hook_error',
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

class CrupyParserNodeDslProductionName(CrupyParserNodeBase):
    """ production name node """
    production_name: str

def dsl_production_name_hook(
    node: CrupyParserNodeBase,
) -> CrupyParserNodeBase:
    """ hook the `crupy_dsl_production_name` production

    @note
    > production -> crupy_dsl_production_name ::= "<[a-z_]+>"
    > only keep the production name and ignore all other information
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'lex_text'
    assert node.seq[1].type == 'lex_rep'
    assert node.seq[2].type == 'lex_text'
    assert len(node.seq[1].rep) >= 1
    rule_name = ''
    for text in node.seq[1].rep:
        assert len(text) == 1
        assert text[0].type == 'lex_text'
        rule_name += text[0].text
    return CrupyParserNodeDslProductionName(
        context         = node.context,
        production_name = rule_name,
    )

def dsl_production_name_hook_error(
    err: CrupyParserBaseException,
) -> NoReturn:
    """ string error hook
    """
    assert err.type == 'lexer_op_seq'
    if err.validated_operation == 0:
        raise CrupyDslParserException(err, 'missing opening chevron')
    if err.validated_operation == 1:
        raise CrupyDslParserException(
            err,
            'production name should only contain alphanumerical and '
            'underscore characters',
        )
    if err.validated_operation == 2:
        raise CrupyDslParserException(err, 'missing enclosing chevron')
    raise CrupyDslParserException(
        err,
        '[internal error] unsupported sequence, too many validated '
        f"operation ({err.validated_operation} > 2)"
    )
