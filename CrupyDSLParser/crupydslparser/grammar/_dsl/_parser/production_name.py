"""
crupydslparser.grammar._dsl._parser.production_name  - DSL parser hook
"""
__all__ = [
    'dsl_production_name_hook',
]

from crupydslparser.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeBaseDslProductionName(CrupyParserNodeBase):
    """ production name node """
    production_name: str

def dsl_production_name_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ hook the `crupy_dsl_production_name` production

    @note
    > production -> crupy_dsl_production_name ::= "<[a-z_]+>"
    > only keep the production name and ignore all other information
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 3
    assert node.seq[0].type == 'lex_text'
    assert node.seq[1].type == 'lex_rep'
    assert node.seq[2].type == 'lex_text'
    assert len(node.seq[1].rep) >= 1
    rule_name = ''
    for text in node.seq[1].rep:
        assert len(text) == 1
        assert text[0].type == 'lex_text'
        rule_name += text[0].text
    return CrupyParserNodeBaseDslProductionName(
        context         = node.stream_context,
        production_name = rule_name,
    )
