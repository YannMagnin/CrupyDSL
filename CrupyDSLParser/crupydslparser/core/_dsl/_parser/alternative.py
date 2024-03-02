"""
crupydslparser.core._dsl._parser.alternative  - DSL alternative hook
"""
__all__ = [
    'dsl_alternative_hook',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeDslAlternative(CrupyParserNode):
    """ alternative node """
    seq:    list[CrupyParserNode]

def dsl_alternative_hook(node: CrupyParserNode) -> CrupyParserNode:
    """ handle "alternative" node
    """
    assert node['name'] == 'lex_rep'
    assert len(node['rep']) >= 1
    node_seq: list[CrupyParserNode] = []
    for seq in node['rep']:
        assert len(seq) == 2
        assert seq[0]['name'] == 'dsl_space'
        assert seq[1]['name'] in [
            'dsl_prod_name',
            'dsl_group',
            'dsl_string',
            'dsl_builtin',
        ]
        node_seq.append(seq[1])
    return CrupyParserNodeDslAlternative(
        parent_node = node,
        seq         = node_seq,
    )
