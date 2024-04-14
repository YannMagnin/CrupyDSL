"""
crupydslparser.grammar._dsl._parser.production  - DSL production hook
"""
__all__ = [
    'dsl_production_hook',
]

from crupydslparser.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeBaseDslProduction(CrupyParserNodeBase):
    """ production node """
    production_name:    str
    statement:          CrupyParserNodeBase

def dsl_production_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle "production" node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 7
    assert node.seq[0].type == 'lex_optional'
    assert node.seq[1].type == 'dsl_production_name'
    assert node.seq[2].type == 'dsl_space'
    assert node.seq[3].type == 'lex_text'
    assert node.seq[3].text == '::='
    assert node.seq[4].type == 'dsl_space'
    assert node.seq[5].type == 'dsl_statement'
    assert node.seq[6].type == 'dsl_eol'
    return CrupyParserNodeBaseDslProduction(
        parent_node     = node,
        production_name = node.seq[1].production_name,
        statement       = node.seq[5],
    )