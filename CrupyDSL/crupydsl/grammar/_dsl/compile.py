"""
crupydsl.grammar._dsl.compil  - compil a grammar shard
"""
__all__ = [
    'dsl_compil_grammar_statement',
]
from typing import Union, Any, cast

from crupydsl.parser._lexer._operation import (
    CrupyDSLLexerOpBase,
    CrupyDSLLexerOpOr,
    CrupyDSLLexerOpSeq,
    CrupyDSLLexerOpProductionCall,
    CrupyDSLLexerOpBuiltin,
    CrupyDSLLexerOpBetween,
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpRep0N,
    CrupyDSLLexerOpRep1N,
    CrupyDSLLexerOpOptional,
)
from crupydsl.parser._lexer._assert import (
    CrupyDSLLexerAssertBase,
    CrupyDSLLexerAssertLookaheadPositive,
    CrupyDSLLexerAssertLookaheadNegative,
)
from crupydsl.grammar._dsl._parser.prod_statement import (
    CrupyDSLParserNodeDslStatement,
)
from crupydsl.grammar._dsl._parser.prod_alternative import (
    CrupyDSLParserNodeDslAlternative,
)
from crupydsl.grammar.exception import CrupyDSLGrammarBaseException

#---
# Internals
#---

# allow too many branches to simplify the tranlation (can be cleaned later)
# also allow access to a private attribute to simplify some operation like
# `CrupyDSLLexerOpRep0N,CrupyDSLLexerAssertLookaheadPositive,...` that support
# multiple operations without explicit `CrupyDSLLexerOpSeq`
# pylint: disable=locally-disabled,W0212,R0911,R0912

def _dsl_compil_grammar_operation(
    operation: Any,
) -> Union[CrupyDSLLexerOpBase,CrupyDSLLexerAssertBase]:
    """ DSL grammar operation handling
    """
    if operation.type == 'dsl_production_name':
        return CrupyDSLLexerOpProductionCall(operation.production_name)
    if operation.type == 'dsl_builtin':
        return CrupyDSLLexerOpBuiltin(operation.kind)
    if operation.type == 'dsl_string':
        return CrupyDSLLexerOpText(operation.text)
    if operation.type == 'dsl_between':
        startop = dsl_compil_grammar_statement(operation.opening)
        endop = dsl_compil_grammar_statement(operation.closing)
        return CrupyDSLLexerOpBetween(
            startop         = startop,
            endop           = endop,
            with_newline    = operation.kind == 'newline',
        )
    if operation.type == 'dsl_group':
        lexerop = dsl_compil_grammar_statement(operation.statement)
        if isinstance(lexerop, CrupyDSLLexerOpSeq):
            if operation.lookahead == 'possitive':
                return CrupyDSLLexerAssertLookaheadPositive(*lexerop._seq)
            if operation.lookahead == 'negative':
                return CrupyDSLLexerAssertLookaheadNegative(*lexerop._seq)
            if operation.operation is None:
                return lexerop
            if operation.operation == 'zero_plus':
                return CrupyDSLLexerOpRep0N(*lexerop._seq)
            if operation.operation == 'one_plus':
                return CrupyDSLLexerOpRep1N(*lexerop._seq)
            if operation.operation == 'optional':
                return CrupyDSLLexerOpOptional(*lexerop._seq)
        else:
            if operation.lookahead == 'possitive':
                return CrupyDSLLexerAssertLookaheadPositive(lexerop)
            if operation.lookahead == 'negative':
                return CrupyDSLLexerAssertLookaheadNegative(lexerop)
            if operation.operation is None:
                return lexerop
            if operation.operation == 'zero_plus':
                return CrupyDSLLexerOpRep0N(lexerop)
            if operation.operation == 'one_plus':
                return CrupyDSLLexerOpRep1N(lexerop)
            if operation.operation == 'optional':
                return CrupyDSLLexerOpOptional(lexerop)
        raise CrupyDSLGrammarBaseException(
            f"dsl_group: operation '{operation.operation}' not supported")
    raise CrupyDSLGrammarBaseException(
        f"unable to translate the DSL operation '{operation.type}'"
        f" ({operation})"
    )

def _dsl_compil_grammar_alternative(
    alternative: CrupyDSLParserNodeDslAlternative,
) -> Union[CrupyDSLLexerOpBase,CrupyDSLLexerAssertBase]:
    """ DSL grammar alternative handling

    @note
    - handle alternative
    - handle seq
    """
    op_list: list[Union[CrupyDSLLexerOpBase,CrupyDSLLexerAssertBase]] = []
    for operation in alternative.seq:
        op_list.append(
            _dsl_compil_grammar_operation(operation),
        )
    if len(op_list) <= 1:
        return op_list[0]
    return CrupyDSLLexerOpSeq(*op_list)

#---
# Public
#---

def dsl_compil_grammar_statement(
    statement: CrupyDSLParserNodeDslStatement,
) -> CrupyDSLLexerOpBase:
    """ DSL grammar compilation

    @note
    - handle statement
    - handle or
    """
    alt_list: list[Union[CrupyDSLLexerOpBase,CrupyDSLLexerAssertBase]] = []
    for alternative in statement.alternatives:
        alt_list.append(
            _dsl_compil_grammar_alternative(
                cast(CrupyDSLParserNodeDslAlternative, alternative),
            ),
        )
    if not alt_list:
        raise CrupyDSLGrammarBaseException(
            'unable to translate the statement: missing alternatives'
        )
    if len(alt_list) > 1:
        return CrupyDSLLexerOpOr(*alt_list)
    if isinstance(alt_list[0], CrupyDSLLexerAssertBase):
        raise CrupyDSLGrammarBaseException(
            'unable to translate the statement: missing lexer operation '
            '(only a assert operation as been detected)'
        )
    return alt_list[0]
