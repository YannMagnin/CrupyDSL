"""
crupydsl.grammar._dsl._parser.alternative  - DSL alternative hook
"""
__all__ = [
    'CrupyDSLParserNodeDslAlternative',
    'dsl_alternative_hook',
]

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeDslAlternative(CrupyDSLParserNodeBase):
    """ alternative node """
    seq:    list[CrupyDSLParserNodeBase]

def dsl_alternative_hook(
    node: CrupyDSLParserNodeBase,
) -> CrupyDSLParserNodeBase:
    """ handle "alternative" node
    """
    assert node.type == 'lex_rep'
    assert len(node.rep) >= 1
    node_seq: list[CrupyDSLParserNodeBase] = []
    for seq in node.rep:
        assert len(seq) == 2
        assert seq[0].type == 'dsl_space'
        assert seq[1].type in [
            'dsl_production_name',
            'dsl_group',
            'dsl_string',
            'dsl_builtin',
            'dsl_between',
        ]
        node_seq.append(seq[1])
    return CrupyDSLParserNodeDslAlternative(
        parent_node = node,
        seq         = node_seq,
    )
