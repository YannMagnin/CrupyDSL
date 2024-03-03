"""
tests.dsl.space - test space productions
"""
__all__ = [
    'CrupyUnittestDslSpace',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._dsl._parser import CRUPY_DSL_PARSER_OBJ

#---
# Public
#---

class CrupyUnittestDslSpace(CrupyUnittestBase):
    """ unittest suite for the `*space*` rules
    """

    #---
    # Public tests
    #---

    def test_simple_lowlevel(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream(' \t\v \\\n')
        node1 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        node2 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        node3 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        node4 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        node5 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        self.assertIsNotNone(node1)
        self.assertIsNotNone(node3)
        self.assertIsNotNone(node4)
        self.assertIsNotNone(node5)
        self.assertIsNone(CRUPY_DSL_PARSER_OBJ.execute('__space'))
        if node1 is None or node2 is None or node3 is None or node4 is None:
            return
        self.assertEqual(node1.type, 'dsl_space')
        self.assertEqual(node2.type, 'dsl_space')
        self.assertEqual(node3.type, 'dsl_space')
        self.assertEqual(node4.type, 'dsl_space')

    def test_space(self) -> None:
        """ space rule """
        CRUPY_DSL_PARSER_OBJ.register_stream(' \t\v \\\na')
        self.assertIsNotNone(CRUPY_DSL_PARSER_OBJ.execute('space'))
        self.assertIsNone(CRUPY_DSL_PARSER_OBJ.execute('space'))
        self.assertEqual(CRUPY_DSL_PARSER_OBJ.stream.read_char(), 'a')
