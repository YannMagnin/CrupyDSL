"""
crupydslparser.core._dsl._parser.statement  - DSL statement hook
"""
__all__ = [
    'dsl_statement_hook',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeDslStatement(CrupyParserNode):
    """ statement node """
    alternatives:    list[CrupyParserNode]

def dsl_statement_hook(node: CrupyParserNode) -> CrupyParserNode:
    """ handle "statement" node
    """
    assert node['name'] == 'lex_seq'
    assert len(node['seq']) == 4
    assert node['seq'][0]['name'] == 'dsl_space'
    assert node['seq'][1]['name'] == 'lex_optional'
    assert node['seq'][2]['name'] == 'dsl_alternative'
    assert node['seq'][3]['name'] == 'lex_rep'
    alternatives = [node['seq'][2]]
    for rep in node['seq'][3]['rep']:
        assert len(rep) == 4
        assert rep[0]['name'] == 'dsl_space'
        assert rep[1]['name'] == 'lex_text'
        assert rep[1]['text'] == '|'
        assert rep[2]['name'] == 'dsl_space'
        assert rep[3]['name'] == 'dsl_alternative'
        alternatives.append(rep[3])
    return CrupyParserNodeDslStatement(
        parent_node     = node,
        alternatives    = alternatives,
    )
