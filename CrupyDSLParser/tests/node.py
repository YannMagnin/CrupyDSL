"""
tests.stream.stream     - stream object unittest
"""
__all__ = [
    'CrupyUnittestNode',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._stream import CrupyStream
from crupydslparser.core.parser import CrupyParserNode

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
        with stream as lexem:
            node = CrupyParserNode(
                stream_ctx  = lexem.validate(),
            )
            self.assertIsNotNone(node)

    def test_custom(self) -> None:
        """ custom tests """
        stream = CrupyStream.from_any('abcd')
        with stream as lexem:
            node = CrupyParserNodeTest(
                stream_ctx  = lexem.validate(),
                name        = 'coucou',
            )
            self.assertIsNotNone(node)
            self.assertEqual(node.type, 'test')
            self.assertEqual(getattr(node, 'name'), 'coucou')
            self.assertEqual(node.name, 'coucou')
            print(node)
