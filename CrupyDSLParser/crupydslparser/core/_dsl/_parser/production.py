"""
crupydslparser.core._dsl._parser.production  - DSL production hook
"""
__all__ = [
    'dsl_production_hook',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeDslProduction(CrupyParserNode):
    """ production node """
    production_name:    str
    statement:          CrupyParserNode

def dsl_production_hook(node: CrupyParserNode) -> CrupyParserNode:
    """ handle "production" node
    """
    assert node['name'] == 'lex_seq'
    assert len(node['seq']) == 7
    assert node['seq'][0]['name'] == 'dsl_space'
    assert node['seq'][1]['name'] == 'dsl_prod_name'
    assert node['seq'][2]['name'] == 'dsl_space'
    assert node['seq'][3]['name'] == 'lex_text'
    assert node['seq'][3]['text'] == '::='
    assert node['seq'][4]['name'] == 'dsl_space'
    assert node['seq'][5]['name'] == 'dsl_statement'
    assert node['seq'][6]['name'] == 'dsl_eol'
    return CrupyParserNodeDslProduction(
        parent_node     = node,
        production_name = node['seq'][1]['production_name'],
        statement       = node['seq'][5],
    )
