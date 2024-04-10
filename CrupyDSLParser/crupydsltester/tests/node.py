"""
tests.stream.stream     - stream object unittest
"""
__all__ = [
    'CrupyUnittestNode',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydsltester._stream import CrupyStream
from crupydsltester.parser import CrupyParserNode

#---
# Public
#---

class CrupyParserNodeTest(CrupyParserNode):
    """ node test """
    name:   str

class CrupyUnittestNode(CrupyUnittestBase):
    """ unittest suit for the crypu stream object
    """

    #---
    # Public tests
    #---

    def test_simple(self) -> None:
        """ simply check the read/peek """
        stream = CrupyStream.from_any('abcd')
        with stream as context:
            node = CrupyParserNode(
                context = context.validate(),
            )
            self.assertIsNotNone(node)

    def test_custom(self) -> None:
        """ custom tests """
        stream = CrupyStream.from_any('abcd')
        with stream as context:
            node = CrupyParserNodeTest(
                context = context.validate(),
                name    = 'coucou',
            )
            self.assertIsNotNone(node)
            self.assertEqual(node.type, 'test')
            self.assertEqual(getattr(node, 'name'), 'coucou')
            self.assertEqual(node.name, 'coucou')
            print(node)
