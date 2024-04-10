"""
crupydslparser._dsl._parser.string  - handle string production
"""
__all__ = [
    'dsl_string_hook',
    'dsl_string_hook_error'
]
from typing import NoReturn

from crupydslparser.parser import (
    CrupyParserNode,
    CrupyParserException,
)

#---
# Public
#---

class CrupyParserNodeDslString(CrupyParserNode):
    """ DSL "string" node """
    text:   str

def dsl_string_hook(node: CrupyParserNode) -> CrupyParserNode:
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

def dsl_string_hook_error(err: CrupyParserException) -> NoReturn:
    """ string error hook
    """
    print('dls string error hook')
    print(err)
    raise err
