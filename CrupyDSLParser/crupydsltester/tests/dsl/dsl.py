"""
tests.dsl.dsl - test dsl productions
"""
__all__ = [
    'CrupyUnittestDslDsl',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydsltester._dsl._parser import CRUPY_DSL_PARSER_OBJ

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
        CRUPY_DSL_PARSER_OBJ.register_stream("<entry> ::= \"yes\" <test>")
        node = CRUPY_DSL_PARSER_OBJ.execute('crupy_dsl')
        self.assertEqual(node.type, 'dsl_entry')
        self.assertEqual(len(node.productions), 1)
        self.assertEqual(node.productions[0].type, 'dsl_production')
        self.assertEqual(node.productions[0].production_name, 'entry')

    def test_simple_dsl_with_spaces(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream("""
            <entry> ::= "yes" <test>
        """)
        node = CRUPY_DSL_PARSER_OBJ.execute('crupy_dsl')
        self.assertEqual(node.type, 'dsl_entry')
        self.assertEqual(len(node.productions), 1)
        self.assertEqual(node.productions[0].type, 'dsl_production')
        self.assertEqual(node.productions[0].production_name, 'entry')

    #def test_multiline_dsl(self) -> None:
    #    """ simple valid case """
    #    CRUPY_DSL_PARSER_OBJ.register_stream("""
    #        <entry> ::= "yes" <test>
    #        <test>  ::= "test"
    #    """)
    #    node = CRUPY_DSL_PARSER_OBJ.execute('crupy_dsl', True)
    #    self.assertIsNotNone(node)
    #    if node is None:
    #        return
    #    self.assertEqual(node.type, 'dsl_entry')
    #    self.assertEqual(len(node.productions), 2)
    #    self.assertEqual(node.productions[0].type, 'production_name')
    #    self.assertEqual(node.productions[0].production_name, 'entry')
    #    self.assertEqual(node.productions[1].type, 'production_name')
    #    self.assertEqual(node.productions[1].production_name, 'test')
