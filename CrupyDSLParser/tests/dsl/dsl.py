"""
tests.dsl.dsl - test dsl productions
"""
__all__ = [
    'CrupyUnittestDslDsl',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._dsl._parser import CRUPY_DSL_PARSER_OBJ

#---
# Public
#---

class CrupyUnittestDslDsl(CrupyUnittestBase):
    """ unittest suite for the `*dsl*` rules
    """

    #---
    # Public tests
    #---

    def test_simple_dsl(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream("""
            <entry> ::= "yes" <test>
            <test>  ::= "test"
        """)
        node = CRUPY_DSL_PARSER_OBJ.execute('crupy_dsl')
        self.assertIsNotNone(node)
        if node is None:
            return
        self.assertEqual(node['name'], 'dsl_entry')
        self.assertEqual(len(node['productions']), 2)
        self.assertEqual(node['productions'][0]['name'], 'production_name')
        self.assertEqual(node['productions'][0]['production_name'], 'entry')
        self.assertEqual(node['productions'][1]['name'], 'production_name')
        self.assertEqual(node['productions'][1]['production_name'], 'test')
