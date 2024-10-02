"""
crupydsl.grammar._dsl._parser.dsl  - DSL dsl hook
"""
__all__ = [
    'CrupyDSLParserNodeDslEntry',
    'dsl_dsl_hook',
]

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeDslEntry(CrupyDSLParserNodeBase):
    """ dsl node """
    productions:    list[CrupyDSLParserNodeBase]

def dsl_dsl_hook(node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
    """ handle "dsl" node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'lex_rep'
    assert node.seq[1].type == 'lex_optional'
    assert node.seq[2].type == 'builtin_eof'
    production_list: list[CrupyDSLParserNodeBase] = []
    for seq in node.seq[0].rep:
        assert len(seq) == 1
        assert seq[0].type == 'dsl_production'
        production_list.append(seq[0])
    return CrupyDSLParserNodeDslEntry(
        parent_node = node,
        productions = production_list,
    )
