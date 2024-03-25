"""
tests.lexer.dsl_production_name - test `crupy_dsl_production_name` rule
"""
__all__ = [
    'CrupyUnittestDslProdName',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._dsl._parser import CRUPY_DSL_PARSER_OBJ

#---
# Public
#---

class CrupyUnittestDslProdName(CrupyUnittestBase):
    """ unittest suite for the `crupy_dsl_production_name` rule
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream('<oui_non><abcd><qwer_')
        node1 = CRUPY_DSL_PARSER_OBJ.execute('production_name', False)
        node2 = CRUPY_DSL_PARSER_OBJ.execute('production_name', False)
        node3 = CRUPY_DSL_PARSER_OBJ.execute('production_name', False)
        self.assertIsNotNone(node1)
        self.assertIsNotNone(node2)
        self.assertIsNone(node3)
        if node1 is None or node2 is None:
            return
        self.assertEqual(node1.type, 'dsl_production_name')
        self.assertEqual(node2.type, 'dsl_production_name')
        self.assertEqual(node1.production_name, 'oui_non')
        self.assertEqual(node2.production_name, 'abcd')
