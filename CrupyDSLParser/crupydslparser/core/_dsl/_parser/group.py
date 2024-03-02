"""
crupydslparser.core._dsl._parser.group  - DSL group hook
"""
__all__ = [
    'dsl_group_hook',
]

from crupydslparser.core.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeDslGroup(CrupyParserNode):
    """ group node """
    lookahead:  str|None
    statement:  CrupyParserNode
    operation:  str|None

def dsl_group_hook(node: CrupyParserNode) -> CrupyParserNode:
    """ handle "group" node
    """
    assert node['name'] == 'lex_seq'
    assert len(node['seq']) == 7
    assert node['seq'][0]['name'] == 'lex_text'
    assert node['seq'][1]['name'] == 'lex_optional'
    assert node['seq'][2]['name'] == 'dsl_space'
    assert node['seq'][3]['name'] == 'dsl_statement'
    assert node['seq'][4]['name'] == 'dsl_space'
    assert node['seq'][5]['name'] == 'lex_text'
    assert node['seq'][6]['name'] == 'lex_optional'
    lookahead: str|None = None
    if node['seq'][1]['seq']:
        assert len(node['seq'][1]['seq']) == 2
        assert node['seq'][1]['seq'][0]['name'] == 'lex_text'
        assert node['seq'][1]['seq'][0]['text'] == '?'
        assert node['seq'][1]['seq'][1]['name'] == 'lex_text'
        assert node['seq'][1]['seq'][1]['text'] in '!='
        lookahead = 'negative'
        if node['seq'][1]['seq'][1]['text'] == '=':
            lookahead = 'positive'
    operation: str|None = None
    if node['seq'][6]['seq']:
        assert len(node['seq'][6]['seq']) == 1
        assert node['seq'][6]['seq'][0]['name'] == 'lex_text'
        assert node['seq'][6]['seq'][0]['text'] in '*+?'
        operation = 'zero_plus'
        if node['seq'][6]['seq'][0]['text'] == '+':
            operation = 'one_plus'
        if node['seq'][6]['seq'][0]['text'] == '?':
            operation = 'optional'
    return CrupyParserNodeDslGroup(
        parent_node = node,
        lookahead   = lookahead,
        statement   = node['seq'][3],
        operation   = operation,
    )
