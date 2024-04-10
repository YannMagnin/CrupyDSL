"""
tests.dsl.production - test production productions
"""
__all__ = [
    'CrupyUnittestDslProduction',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydsltester._dsl._parser import CRUPY_DSL_PARSER_OBJ

#---
# Public
#---

class CrupyUnittestDslProduction(CrupyUnittestBase):
    """ unittest suite for the `*production*` rules
    """

    #---
    # Public tests
    #---

    def test_simple_test(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream('<entry> ::= "allo?"')
        node = CRUPY_DSL_PARSER_OBJ.execute('production')
        self.assertEqual(node.type, 'dsl_production')
        self.assertEqual(node.production_name, 'entry')
        self.assertEqual(node.statement.type, 'dsl_statement')
        self.assertEqual(len(node.statement.alternatives), 1)

    def test_simple_test_with_space(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream("""
            <entry> ::= "allo?"
        """)
        node = CRUPY_DSL_PARSER_OBJ.execute('production')
        self.assertEqual(node.type, 'dsl_production')
        self.assertEqual(node.production_name, 'entry')
        self.assertEqual(node.statement.type, 'dsl_statement')
        self.assertEqual(len(node.statement.alternatives), 1)

    def test_multiple_production(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream("""
            <entry> ::= "allo?" <oui>
            <oui>   ::= "non"
        """)
        node = CRUPY_DSL_PARSER_OBJ.execute('production')
        self.assertEqual(node.type, 'dsl_production')
        self.assertEqual(node.production_name, 'entry')
        self.assertEqual(node.statement.type, 'dsl_statement')
        self.assertEqual(len(node.statement.alternatives), 1)
        node = CRUPY_DSL_PARSER_OBJ.execute('production')
        self.assertEqual(node.type, 'dsl_production')
        self.assertEqual(node.production_name, 'oui')
        self.assertEqual(node.statement.type, 'dsl_statement')
        self.assertEqual(len(node.statement.alternatives), 1)

    #def test_simple_error(self) -> None:
    #    """ simple valid case """
    #    CRUPY_DSL_PARSER_OBJ.register_stream("""
    #        <entry> ::= "allo?
    #    """)
    #    node = CRUPY_DSL_PARSER_OBJ.execute('production', True)
