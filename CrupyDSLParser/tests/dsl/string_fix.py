"""
tests.dsl.string_fix - test string productions
"""
__all__ = [
    'CrupyUnittestDslString',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._dsl._parser import CRUPY_DSL_PARSER_OBJ

#---
# Public
#---

class CrupyUnittestDslString(CrupyUnittestBase):
    """ unittest suite for the `*string*` rules
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream(r'"667 oui ~# \\ dslk"')
        node = CRUPY_DSL_PARSER_OBJ.execute('string')
        self.assertIsNotNone(node)
        if node is None:
            return
        self.assertEqual(node.type, 'dsl_string')
        self.assertEqual(node.text, r'667 oui ~# \ dslk')

    def test_escape(self) -> None:
        """ test escaping """
        CRUPY_DSL_PARSER_OBJ.register_stream('"\\"\\\\"')
        node = CRUPY_DSL_PARSER_OBJ.execute('string')
        self.assertIsNotNone(node)
        if node is None:
            return
        self.assertEqual(node.type, 'dsl_string')
        self.assertEqual(node.text, '"\\')
