"""
tests.dsl.builtin - test builtin production
"""
__all__ = [
    'CrupyUnittestDslBuiltin',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ

#---
# Public
#---

class CrupyUnittestDslBuiltin(CrupyUnittestBase):
    """ unittest suite for the `builtin` rule
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream(':digit::any:')
        node0 = CRUPY_DSL_PARSER_OBJ.execute('builtin')
        node1 = CRUPY_DSL_PARSER_OBJ.execute('builtin')
        self.assertIsNotNone(node0)
        self.assertIsNotNone(node1)
        self.assertEqual(node0.type, 'dsl_builtin')
        self.assertEqual(node0.kind, 'digit')
        self.assertEqual(node1.type, 'dsl_builtin')
        self.assertEqual(node1.kind, 'any')
