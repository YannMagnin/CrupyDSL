"""
crupydsl.grammar._dsl._parser.dsl  - DSL dsl hook
"""
__all__ = [
    'CrupyParserNodeDslEntry',
    'dsl_dsl_hook',
]

from crupydsl.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeDslEntry(CrupyParserNodeBase):
    """ dsl node """
    productions:    list[CrupyParserNodeBase]

def dsl_dsl_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle "dsl" node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'lex_rep'
    assert node.seq[1].type == 'lex_optional'
    assert node.seq[2].type == 'builtin_eof'
    production_list: list[CrupyParserNodeBase] = []
    for seq in node.seq[0].rep:
        assert len(seq) == 1
        assert seq[0].type == 'dsl_production'
        production_list.append(seq[0])
    return CrupyParserNodeDslEntry(
        parent_node = node,
        productions = production_list,
    )
