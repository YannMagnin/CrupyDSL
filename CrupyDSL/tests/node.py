"""
tests.stream.stream     - stream object unittest
"""
from typing import List, Dict, Union

from crupydsl.parser._stream.stream import CrupyDSLStream
from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Internals
#---

class _CrupyDSLParserNodeTest(CrupyDSLParserNodeBase):
    """ node test """
    name:   str

class _CrupyDSLParserNodeSibling(CrupyDSLParserNodeBase):
    """ node test 2 """
    sibling_0: CrupyDSLParserNodeBase
    sibling_1: CrupyDSLParserNodeBase

class _CrupyDSLParserNodeList(CrupyDSLParserNodeBase):
    """ node test 2 (force outdated typing description) """
    list_test: List[Union[int,str,CrupyDSLParserNodeBase]]

class _CrupyDSLParserNodeDict(CrupyDSLParserNodeBase):
    """ node test dict """
    dict_test: Dict[str, Union[int,str,CrupyDSLParserNodeBase]]

#---
# Public
#---

def test_simple() -> None:
    """ simply check the read/peek
    """
    stream = CrupyDSLStream.from_any('abcd')
    with stream as context:
        node = _CrupyDSLParserNodeTest(
            context = context.validate(),
        )
        assert node is not None

def test_custom() -> None:
    """ custom tests
    """
    stream = CrupyDSLStream.from_any('abcd')
    with stream as context:
        node = _CrupyDSLParserNodeTest(
            context = context.validate(),
            name    = 'coucou',
        )
        assert node is not None
        assert node.type == 'test'
        assert getattr(node, 'name') == 'coucou'
        assert node.name == 'coucou'

def test_show() -> None:
    """ debug tests
    """
    stream = CrupyDSLStream.from_any('abcd')
    with stream as context:
        context_obj = context.validate()
    node0 = _CrupyDSLParserNodeTest(
        context = context_obj,
        name    = 'coucou',
    )
    node1 = _CrupyDSLParserNodeSibling(
        context     = context_obj,
        sibling_0   = node0,
        sibling_1   = node0,
    )
    node2 = _CrupyDSLParserNodeList(
        context     = context_obj,
        list_test   = [0, 'ekip', node0],
    )
    node3 = _CrupyDSLParserNodeDict(
        context     = context_obj,
        dict_test   = {'0': 0, '1': 'ekip', 'test': node0},
    )
    ctxstr = \
        'CrupyDSLStreamContext(index_start=0,index=0,lineno=1,column=1)'
    assert node0.show() == (
         '_CrupyDSLParserNodeTest(\n'
         '    type    = \'test\',\n'
        f'    context = {ctxstr},\n'
         '    name    = \'coucou\',\n'
         ')'
    )
    assert node1.show() == (
         '_CrupyDSLParserNodeSibling(\n'
         '    type    = \'sibling\',\n'
        f'    context = {ctxstr},\n'
         '    sibling_0   = _CrupyDSLParserNodeTest(\n'
         '        type    = \'test\',\n'
        f'        context = {ctxstr},\n'
         '        name    = \'coucou\',\n'
         '    ),\n'
         '    sibling_1   = _CrupyDSLParserNodeTest(\n'
         '        type    = \'test\',\n'
        f'        context = {ctxstr},\n'
         '        name    = \'coucou\',\n'
         '    ),\n'
         ')'
    )
    assert node2.show() == (
        '_CrupyDSLParserNodeList(\n'
         '    type    = \'list\',\n'
        f'    context = {ctxstr},\n'
         '    list_test   = [ # 3 entries\n'
         '        0,\n'
         '        \'ekip\',\n'
         '        _CrupyDSLParserNodeTest(\n'
         '            type    = \'test\',\n'
        f'            context = {ctxstr},\n'
         '            name    = \'coucou\',\n'
         '        ),\n'
         '    ],\n'
         ')'
    )
    assert node3.show() == (
        '_CrupyDSLParserNodeDict(\n'
         '    type    = \'dict\',\n'
        f'    context = {ctxstr},\n'
         '    dict_test   = { # 3 entries\n'
         '        \'0\' : 0,\n'
         '        \'1\' : \'ekip\',\n'
         '        \'test\' : _CrupyDSLParserNodeTest(\n'
         '            type    = \'test\',\n'
        f'            context = {ctxstr},\n'
         '            name    = \'coucou\',\n'
         '        ),\n'
         '    },\n'
         ')'
    )
