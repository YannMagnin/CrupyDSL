"""
tests.dsl.alternative - test alternative productions
"""
__all__ = [
    'CrupyUnittestDslAlternative',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._dsl._parser import CRUPY_DSL_PARSER_OBJ

#---
# Public
#---

class CrupyUnittestDslAlternative(CrupyUnittestBase):
    """ unittest suite for the `*alternative*` rules
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream(
            '<test_oui> "test" :number: (?!"oui?")?'
        )
        node = CRUPY_DSL_PARSER_OBJ.execute('alternative')
        self.assertIsNotNone(node)
        if node is None:
            return
        self.assertEqual(node['name'], 'dsl_alternative')
        self.assertEqual(len(node['seq']), 4)
        self.assertEqual(node['seq'][0]['name'], 'dsl_prod_name')
        self.assertEqual(node['seq'][0]['production_name'], 'test_oui')
        self.assertEqual(node['seq'][1]['name'], 'dsl_string')
        self.assertEqual(node['seq'][1]['text'], 'test')
        self.assertEqual(node['seq'][2]['name'], 'dsl_builtin')
        self.assertEqual(node['seq'][2]['kind'], 'number')
        self.assertEqual(node['seq'][3]['name'], 'dsl_group')
        self.assertEqual(node['seq'][3]['lookahead'], 'negative')
        self.assertEqual(node['seq'][3]['operation'], 'optional')
        self.assertEqual(
            node['seq'][3]['statement']['name'],
            'dsl_statement',
        )
