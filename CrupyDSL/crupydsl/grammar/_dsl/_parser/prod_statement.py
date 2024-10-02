"""
crupydsl.grammar._dsl._parser.statement  - DSL statement hook
"""
__all__ = [
    'CrupyDSLParserNodeDslStatement',
    'dsl_statement_hook',
]

from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeDslStatement(CrupyDSLParserNodeBase):
    """ statement node """
    alternatives:    list[CrupyDSLParserNodeBase]

def dsl_statement_hook(node: CrupyDSLParserNodeBase) -> CrupyDSLParserNodeBase:
    """ handle "statement" node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 4
    assert node.seq[0].type == 'dsl_space'
    assert node.seq[1].type == 'lex_optional'
    assert node.seq[2].type == 'dsl_alternative'
    assert node.seq[3].type == 'lex_rep'
    alternatives = [node.seq[2]]
    for rep in node.seq[3].rep:
        assert len(rep) == 4
        assert rep[0].type == 'dsl_space'
        assert rep[1].type == 'lex_text'
        assert rep[1].text == '|'
        assert rep[2].type == 'dsl_space'
        assert rep[3].type == 'dsl_alternative'
        alternatives.append(rep[3])
    return CrupyDSLParserNodeDslStatement(
        parent_node     = node,
        alternatives    = alternatives,
    )
