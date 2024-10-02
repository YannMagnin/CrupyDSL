"""
tests.stream.stream     - stream object unittest
"""
from crupydsl.parser._stream.stream import CrupyDSLStream
from crupydsl.parser import CrupyDSLParserNodeBase

#---
# Public
#---

class CrupyDSLParserNodeTest(CrupyDSLParserNodeBase):
    """ node test """
    name:   str

def test_simple() -> None:
    """ simply check the read/peek
    """
    stream = CrupyDSLStream.from_any('abcd')
    with stream as context:
        node = CrupyDSLParserNodeTest(
            context = context.validate(),
        )
        assert node is not None

def test_custom() -> None:
    """ custom tests
    """
    stream = CrupyDSLStream.from_any('abcd')
    with stream as context:
        node = CrupyDSLParserNodeTest(
            context = context.validate(),
            name    = 'coucou',
        )
        assert node is not None
        assert node.type == 'test'
        assert getattr(node, 'name') == 'coucou'
        assert node.name == 'coucou'
        print(node)
