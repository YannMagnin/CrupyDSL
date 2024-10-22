"""
crupydsl.grammar._dsl._parser.production  - DSL production hook
"""
__all__ = [
    'CrupyDSLParserNodeDslProduction',
    'dsl_production_hook',
    'dsl_production_hook_error',
]
from crupydsl.parser import CrupyDSLParserNodeBase
from crupydsl.parser.exception import CrupyDSLParserBaseException
from crupydsl.grammar._dsl._parser.exception import (
    CrupyDSLParserException,
)

# Allow too many return statement
# pylint: disable=locally-disabled,R0911

#---
# Public
#---

class CrupyDSLParserNodeDslProduction(CrupyDSLParserNodeBase):
    """ production node """
    production_name:    str
    statement:          CrupyDSLParserNodeBase

def dsl_production_hook(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
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
    return CrupyDSLParserNodeDslProduction(
        parent_node     = node,
        production_name = node.seq[1].production_name,
        statement       = node.seq[5],
    )

def dsl_production_hook_error(
    err: CrupyDSLParserBaseException,
) -> CrupyDSLParserBaseException:
    """ string error hook
    """
    assert err.type == 'lexer_op_seq'
    if err.validated_operation == 1:
        return err
    if err.validated_operation == 2:
        return CrupyDSLParserException(
            err,
            'missing space between production name and equal sign',
        )
    if err.validated_operation == 3:
        return CrupyDSLParserException(err, 'missing enclosing quote')
    if err.validated_operation == 4:
        return CrupyDSLParserException(
            err,
            'missing space between equal sign and statement',
        )
    if err.validated_operation == 5:
        return err
    if err.validated_operation == 6:
        return CrupyDSLParserException(
            err,
            'missing an end-of-line or and end-of-file to validate '
            'the production',
        )
    return CrupyDSLParserException(
        err,
        '[internal error] unsupported sequence, too many validated '
        f"operation ({err.validated_operation})"
    )
