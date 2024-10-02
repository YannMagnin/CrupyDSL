"""
crupydsl.grammar._dsl._parser.production  - DSL production hook
"""
__all__ = [
    'CrupyParserNodeDslProduction',
    'dsl_production_hook',
    'dsl_production_hook_error',
]
from typing import NoReturn

from crupydsl.parser import CrupyParserNodeBase
from crupydsl.parser.exception import CrupyParserBaseException
from crupydsl.grammar._dsl._parser.exception import (
    CrupyDslParserException,
)

#---
# Public
#---

class CrupyParserNodeDslProduction(CrupyParserNodeBase):
    """ production node """
    production_name:    str
    statement:          CrupyParserNodeBase

def dsl_production_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle "production" node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 7
    assert node.seq[0].type == 'lex_optional'
    assert node.seq[1].type == 'dsl_production_name'
    assert node.seq[2].type == 'dsl_space'
    assert node.seq[3].type == 'lex_text'
    assert node.seq[3].text == '::='
    assert node.seq[4].type == 'dsl_space'
    assert node.seq[5].type == 'dsl_statement'
    assert node.seq[6].type == 'dsl_eol'
    return CrupyParserNodeDslProduction(
        parent_node     = node,
        production_name = node.seq[1].production_name,
        statement       = node.seq[5],
    )

def dsl_production_hook_error(err: CrupyParserBaseException) -> NoReturn:
    """ string error hook
    """
    assert err.type == 'lexer_op_seq'
    if err.validated_operation == 1:
        raise err
    if err.validated_operation == 2:
        raise CrupyDslParserException(
            err,
            'missing space between production name and equal sign',
        )
    if err.validated_operation == 3:
        raise CrupyDslParserException(err, 'missing enclosing quote')
    if err.validated_operation == 4:
        raise CrupyDslParserException(
            err,
            'missing space between equal sign and statement',
        )
    if err.validated_operation == 5:
        raise err
    if err.validated_operation == 6:
        raise CrupyDslParserException(
            err,
            'missing an end-of-line or and end-of-file to validate '
            'the production',
        )
    raise CrupyDslParserException(
        err,
        '[internal error] unsupported sequence, too many validated '
        f"operation ({err.validated_operation})"
    )
