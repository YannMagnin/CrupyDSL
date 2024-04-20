"""
crupydslparser.grammar._dsl._parser.alternative  - DSL alternative hook
"""
__all__ = [
    'dsl_alternative_hook',
]

from crupydslparser.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeBaseDslAlternative(CrupyParserNodeBase):
    """ alternative node """
    seq:    list[CrupyParserNodeBase]

def dsl_alternative_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle "alternative" node
    """
    assert node.type == 'lex_rep'
    assert len(node.rep) >= 1
    node_seq: list[CrupyParserNodeBase] = []
    for seq in node.rep:
        assert len(seq) == 2
        assert seq[0].type == 'dsl_space'
        assert seq[1].type in [
            'dsl_production_name',
            'dsl_group',
            'dsl_string',
            'dsl_builtin',
        ]
        node_seq.append(seq[1])
    return CrupyParserNodeBaseDslAlternative(
        parent_node = node,
        seq         = node_seq,
    )
