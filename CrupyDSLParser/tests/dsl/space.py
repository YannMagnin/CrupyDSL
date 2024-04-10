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
        CRUPY_DSL_PARSER_OBJ.register_stream(' \t \\\n')
        node1 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        node2 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        node3 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        node4 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        self.assertEqual(node1.type, 'dsl_space')
        self.assertEqual(node2.type, 'dsl_space')
        self.assertEqual(node3.type, 'dsl_space')
        self.assertEqual(node4.type, 'dsl_space')

    def test_space(self) -> None:
        """ space rule """
        CRUPY_DSL_PARSER_OBJ.register_stream(' \t \\\na')
        self.assertIsNotNone(CRUPY_DSL_PARSER_OBJ.execute('space'))
        with CRUPY_DSL_PARSER_OBJ.stream as context:
            self.assertEqual(context.read_char(), 'a')
