"""
crupydslparser._dsl._parser.string  - handle string production
"""
__all__ = [
    'dsl_string_hook',
    'dsl_string_hook_error'
]
from typing import NoReturn

from crupydslparser.parser.node import CrupyParserNodeBase
from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

class CrupyParserNodeDslString(CrupyParserNodeBase):
    """ DSL "string" node """
    text:   str

def dsl_string_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle `string` node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'lex_text'
    assert node.seq[1].type == 'lex_rep'
    assert node.seq[2].type == 'lex_text'
    assert node.seq[0].text == '"'
    assert node.seq[2].text == '"'
    text = ''
    for seq in node.seq[1].rep:
        assert len(seq) == 1
        assert seq[0].type == 'lex_text'
        text += seq[0].text
    return CrupyParserNodeDslString(
        parent_node = node,
        text        = text,
    )

def dsl_string_hook_error(err: CrupyParserBaseException) -> NoReturn:
    """ string error hook
    """
    assert err.type == 'lexer_op_seq'
    if err.validated_operation == 0:
        raise CrupyParserBaseException(
            'Parsing exception occured:\n'
            '\n'
            f"{err.context.generate_error_log()}\n"
            '\n'
            'SyntaxError: missing starting quote'
        )
    if err.validated_operation == 1:
        raise CrupyParserBaseException(
            'Parsing exception occured:\n'
            '\n'
            f"{err.context.generate_error_log()}\n"
            '\n'
            'SyntaxError: unable to capture string content'
        )
    if err.validated_operation == 2:
        raise CrupyParserBaseException(
            'Parsing exception occured:\n'
            '\n'
            f"{err.context.generate_error_log()}\n"
            '\n'
            'SyntaxError: missing enclosing quote'
        )
    raise CrupyParserBaseException(
        'Parsing exception occured:\n'
        '\n'
        f"{err.context.generate_error_log()}\n"
        '\n'
        'InternalError: unsupported sequence, too many validated '
        f"operation ({err.validated_operation} > 2)"
    )
