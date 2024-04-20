"""
crupydslparser.grammar._dsl._parser.group  - DSL group hook
"""
__all__ = [
    'dsl_group_hook',
]

from crupydslparser.parser import CrupyParserNodeBase

#---
# Public
#---

class CrupyParserNodeBaseDslGroup(CrupyParserNodeBase):
    """ group node """
    lookahead:  str|None
    statement:  CrupyParserNodeBase
    operation:  str|None

def dsl_group_hook(node: CrupyParserNodeBase) -> CrupyParserNodeBase:
    """ handle "group" node
    """
    assert node.type == 'lex_seq'
    assert len(node.seq) == 7
    assert node.seq[0].type == 'lex_text'
    assert node.seq[1].type == 'lex_optional'
    assert node.seq[2].type == 'dsl_space'
    assert node.seq[3].type == 'dsl_statement'
    assert node.seq[4].type == 'dsl_space'
    assert node.seq[5].type == 'lex_text'
    assert node.seq[6].type == 'lex_optional'
    lookahead: str|None = None
    if node.seq[1].seq:
        assert len(node.seq[1].seq) == 2
        assert node.seq[1].seq[0].type == 'lex_text'
        assert node.seq[1].seq[0].text == '?'
        assert node.seq[1].seq[1].type == 'lex_text'
        assert node.seq[1].seq[1].text in '!='
        lookahead = 'negative'
        if node.seq[1].seq[1].text == '=':
            lookahead = 'positive'
    operation: str|None = None
    if node.seq[6].seq:
        assert len(node.seq[6].seq) == 1
        assert node.seq[6].seq[0].type == 'lex_text'
        assert node.seq[6].seq[0].text in '*+?'
        operation = 'zero_plus'
        if node.seq[6].seq[0].text == '+':
            operation = 'one_plus'
        if node.seq[6].seq[0].text == '?':
            operation = 'optional'
    return CrupyParserNodeBaseDslGroup(
        parent_node = node,
        lookahead   = lookahead,
        statement   = node.seq[3],
        operation   = operation,
    )
