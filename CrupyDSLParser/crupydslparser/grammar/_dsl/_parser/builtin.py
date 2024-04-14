"""
crupydslparser.grammar._dsl._parser.builtin  - DSL builtin hook
"""
__all__ = [
    'dsl_builtin_hook',
]

from crupydslparser.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeBaseDslBuiltin(CrupyParserNodeBase):
    """ builtin node
    """
    kind:   str

def dsl_builtin_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle "builtin" node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'lex_text'
    assert node.seq[0].text == ':'
    assert node.seq[2].type == 'lex_text'
    assert node.seq[2].text == ':'
    assert node.seq[1].type == 'lex_rep'
    kind = ''
    for text in node.seq[1].rep:
        assert len(text) == 1
        assert text[0].type == 'lex_text'
        kind += text[0].text
    return CrupyParserNodeBaseDslBuiltin(
        parent_node = node,
        kind        = kind,
    )
