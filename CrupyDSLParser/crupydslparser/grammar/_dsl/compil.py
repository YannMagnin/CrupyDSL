"""
crupydslparser.grammar._dsl.compil  - compil a grammar shard
"""
__all__ = [
    'dsl_compil_grammar_statement',
]
from typing import Any

from crupydslparser.parser._lexer._operation import (
    CrupyLexerOpBase,
    CrupyLexerOpOr,
    CrupyLexerOpSeq,
    CrupyLexerOpProductionCall,
    CrupyLexerOpBuiltin,
    CrupyLexerOpText,
    CrupyLexerOpRep0N,
    CrupyLexerOpRep1N,
    CrupyLexerOpOptional,
)
from crupydslparser.parser._lexer._assert import (
    CrupyLexerAssertBase,
    CrupyLexerAssertLookaheadPositive,
    CrupyLexerAssertLookaheadNegative,
)
from crupydslparser.grammar._dsl._parser._statement import (
    CrupyParserNodeDslStatement,
)
from crupydslparser.grammar._dsl._parser._alternative import (
    CrupyParserNodeDslAlternative,
)
from crupydslparser.grammar.exception import CrupyGrammarException

#---
# Internals
#---

def _dsl_compil_grammar_operation(
    operation: Any,
) -> CrupyLexerOpBase|CrupyLexerAssertBase:
    """ DSL grammar operation handling
    """
    if operation.type == 'dsl_production_name':
        return CrupyLexerOpProductionCall(operation.production_name)
    if operation.type == 'dsl_builtin':
        return CrupyLexerOpBuiltin(operation.kind)
    if operation.type == 'dsl_string':
        return CrupyLexerOpText(operation.text)
    if operation.type == 'dsl_group':
        lexerop = dsl_compil_grammar_statement(operation.statement)
        if operation.lookahead == 'possitive':
            return CrupyLexerAssertLookaheadPositive(lexerop)
        if operation.lookahead == 'negative':
            return CrupyLexerAssertLookaheadNegative(lexerop)
        if operation.operation == 'zero_plus':
            return CrupyLexerOpRep0N(lexerop)
        if operation.operation == 'one_plus':
            return CrupyLexerOpRep1N(lexerop)
        if operation.operation == 'optional':
            return CrupyLexerOpOptional(lexerop)
        raise CrupyGrammarException(
            f"dsl_group: operation '{operation.operation}' not supported")
    raise CrupyGrammarException(
        f"unable to translate the DSL operation '{operation.type}'"
        f" ({operation})"
    )

def _dsl_compil_grammar_alternative(
    alternative: CrupyParserNodeDslAlternative,
) -> CrupyLexerOpBase|CrupyLexerAssertBase:
    """ DSL grammar alternative handling

    @note
    - handle alternative
    - handle seq
    """
    op_list: list[CrupyLexerOpBase|CrupyLexerAssertBase] = []
    for operation in alternative.seq:
        op_list.append(
            _dsl_compil_grammar_operation(operation),
        )
    if len(op_list) <= 0:
        return op_list[0]
    return CrupyLexerOpSeq(*op_list)

#---
# Public
#---

def dsl_compil_grammar_statement(
    statement: CrupyParserNodeDslStatement,
) -> CrupyLexerOpBase:
    """ DSL grammar compilation

    @note
    - handle statement
    - handle or
    """
    alt_list: list[CrupyLexerOpBase|CrupyLexerAssertBase] = []
    for alternative in statement.alternatives:
        alt_list.append(
            _dsl_compil_grammar_alternative(alternative),
        )
    if not alt_list:
        raise CrupyGrammarException(
            'unable to translate the statement: missing alternatives'
        )
    if len(alt_list) > 1:
        return CrupyLexerOpOr(*alt_list)
    if isinstance(alt_list[0], CrupyLexerAssertBase):
        raise CrupyGrammarException(
            'unable to translate the statement: missing lexer operation '
            '(only a assert operation as been detected)'
        )
    return alt_list[0]
