"""
tests.dsl.statement - test statement productions
"""
__all__ = [
    'CrupyUnittestDslStatement',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._dsl._parser import CRUPY_DSL_PARSER_OBJ

#---
# Public
#---

class CrupyUnittestDslStatement(CrupyUnittestBase):
    """ unittest suite for the `*statement*` rules
    """

    #---
    # Public tests
    #---

    def test_one_line(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream(
            '<test_oui> | "coucou" | :any: <ekip>\n'
        )
        node = CRUPY_DSL_PARSER_OBJ.execute('statement')
        self.assertIsNotNone(node)
        if node is None:
            return
        self.assertEqual(node['name'], 'dsl_statement')
        self.assertEqual(len(node['alternatives']), 3)
        alts = node['alternatives']
        self.assertEqual(alts[0]['name'], 'dsl_alternative')
        self.assertEqual(alts[1]['name'], 'dsl_alternative')
        self.assertEqual(alts[2]['name'], 'dsl_alternative')
        self.assertEqual(len(alts[0]['seq']), 1)
        self.assertEqual(len(alts[1]['seq']), 1)
        self.assertEqual(len(alts[2]['seq']), 2)
        self.assertEqual(alts[0]['seq'][0]['name'], 'dsl_prod_name')
        self.assertEqual(alts[1]['seq'][0]['name'], 'dsl_string')
        self.assertEqual(alts[2]['seq'][0]['name'], 'dsl_builtin')
        self.assertEqual(alts[2]['seq'][1]['name'], 'dsl_prod_name')

    def test_multiple_line(self) -> None:
        """ test multiple line """
        CRUPY_DSL_PARSER_OBJ.register_stream(r""" \
            | <test_oui> \
            | "coucou" \
            | :any: <coucou>
        """)
        node = CRUPY_DSL_PARSER_OBJ.execute('statement')
        self.assertIsNotNone(node)
        if node is None:
            return
        self.assertEqual(node['name'], 'dsl_statement')
        self.assertEqual(len(node['alternatives']), 3)
        alts = node['alternatives']
        self.assertEqual(alts[0]['name'], 'dsl_alternative')
        self.assertEqual(alts[1]['name'], 'dsl_alternative')
        self.assertEqual(alts[2]['name'], 'dsl_alternative')
        self.assertEqual(len(alts[0]['seq']), 1)
        self.assertEqual(len(alts[1]['seq']), 1)
        self.assertEqual(len(alts[2]['seq']), 2)
        self.assertEqual(alts[0]['seq'][0]['name'], 'dsl_prod_name')
        self.assertEqual(alts[1]['seq'][0]['name'], 'dsl_string')
        self.assertEqual(alts[2]['seq'][0]['name'], 'dsl_builtin')
        self.assertEqual(alts[2]['seq'][1]['name'], 'dsl_prod_name')
