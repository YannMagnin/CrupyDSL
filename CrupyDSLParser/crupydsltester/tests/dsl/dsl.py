"""
tests.dsl.dsl - test dsl productions
"""
__all__ = [
    'CrupyUnittestDslDsl',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydslparser.parser import CrupyParserBaseException

#---
# Public
#---

class CrupyUnittestDslDsl(CrupyUnittestBase):
    """ unittest suite for the `*dsl*` rules
    """

    #---
    # Public tests
    #---

    ## fonctional

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

    def test_multiline_dsl(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream("""
            <entry> ::= "yes" <test>
            <test>  ::= "test"
        """)
        node = CRUPY_DSL_PARSER_OBJ.execute('crupy_dsl')
        self.assertEqual(node.type, 'dsl_entry')
        self.assertEqual(len(node.productions), 2)
        self.assertEqual(node.productions[0].type, 'dsl_production')
        self.assertEqual(node.productions[0].production_name, 'entry')
        self.assertEqual(node.productions[1].type, 'dsl_production')
        self.assertEqual(node.productions[1].production_name, 'test')

    ## error

    def test_error_broken_production(self) -> None:
        """ test error """
        CRUPY_DSL_PARSER_OBJ.register_stream('aaaaaa')
        err = self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'crupy_dsl'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 1\n'
                'aaaaaa\n'
                '^\n'
                'SyntaxError: missing opening chevron',
        )
        self.assertEqual(err.reason, 'missing opening chevron')
