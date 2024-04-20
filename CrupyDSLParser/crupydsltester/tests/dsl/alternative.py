"""
tests.dsl.alternative - test alternative productions
"""
__all__ = [
    'CrupyUnittestDslAlternative',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ

#---
# Public
#---

class CrupyUnittestDslAlternative(CrupyUnittestBase):
    """ unittest suite for the `*alternative*` rules
    """

    #---
    # Public tests
    #---

    def test_prodname(self) -> None:
        """ test """
        CRUPY_DSL_PARSER_OBJ.register_stream('<test_oui>')
        node = CRUPY_DSL_PARSER_OBJ.execute('alternative')
        self.assertEqual(node.type, 'dsl_alternative')
        self.assertEqual(len(node.seq), 1)
        self.assertEqual(node.seq[0].type, 'dsl_production_name')
        self.assertEqual(node.seq[0].production_name, 'test_oui')

    def test_string(self) -> None:
        """ test """
        CRUPY_DSL_PARSER_OBJ.register_stream('"667ekip"')
        node = CRUPY_DSL_PARSER_OBJ.execute('alternative')
        self.assertEqual(node.type, 'dsl_alternative')
        self.assertEqual(len(node.seq), 1)
        self.assertEqual(node.seq[0].type, 'dsl_string')
        self.assertEqual(node.seq[0].text, '667ekip')

    def test_builtin(self) -> None:
        """ test """
        CRUPY_DSL_PARSER_OBJ.register_stream(':any:')
        node = CRUPY_DSL_PARSER_OBJ.execute('alternative')
        self.assertEqual(node.type, 'dsl_alternative')
        self.assertEqual(len(node.seq), 1)
        self.assertEqual(node.seq[0].type, 'dsl_builtin')
        self.assertEqual(node.seq[0].kind, 'any')

    def test_simple_success(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream(
            '<test_oui> "test" :number: (?!"oui?")?'
        )
        node = CRUPY_DSL_PARSER_OBJ.execute('alternative')
        self.assertEqual(node.type, 'dsl_alternative')
        self.assertEqual(len(node.seq), 4)
        self.assertEqual(node.seq[0].type, 'dsl_production_name')
        self.assertEqual(node.seq[0].production_name, 'test_oui')
        self.assertEqual(node.seq[1].type, 'dsl_string')
        self.assertEqual(node.seq[1].text, 'test')
        self.assertEqual(node.seq[2].type, 'dsl_builtin')
        self.assertEqual(node.seq[2].kind, 'number')
        self.assertEqual(node.seq[3].type, 'dsl_group')
        self.assertEqual(node.seq[3].lookahead, 'negative')
        self.assertEqual(node.seq[3].operation, 'optional')
        self.assertEqual(
            node.seq[3].statement.type,
            'dsl_statement',
        )
