"""
tests.dsl.statement - test statement productions
"""
__all__ = [
    'CrupyUnittestDslStatement',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

class CrupyUnittestDslStatement(CrupyUnittestBase):
    """ unittest suite for the `*statement*` rules
    """

    #---
    # Public tests
    #---

    ## fonctional

    def test_prodname(self) -> None:
        """ test """
        CRUPY_DSL_PARSER_OBJ.register_stream('<test_oui>')
        node = CRUPY_DSL_PARSER_OBJ.execute('statement')
        self.assertEqual(node.type, 'dsl_statement')

    def test_one_line(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream(
            '<test_oui> | "coucou" | :any: <ekip>\n'
        )
        node = CRUPY_DSL_PARSER_OBJ.execute('statement')
        self.assertEqual(node.type, 'dsl_statement')
        self.assertEqual(len(node.alternatives), 3)
        alts = node.alternatives
        self.assertEqual(alts[0].type, 'dsl_alternative')
        self.assertEqual(alts[1].type, 'dsl_alternative')
        self.assertEqual(alts[2].type, 'dsl_alternative')
        self.assertEqual(len(alts[0].seq), 1)
        self.assertEqual(len(alts[1].seq), 1)
        self.assertEqual(len(alts[2].seq), 2)
        self.assertEqual(alts[0].seq[0].type, 'dsl_production_name')
        self.assertEqual(alts[1].seq[0].type, 'dsl_string')
        self.assertEqual(alts[2].seq[0].type, 'dsl_builtin')
        self.assertEqual(alts[2].seq[1].type, 'dsl_production_name')

    def test_multiple_line(self) -> None:
        """ test multiple line """
        CRUPY_DSL_PARSER_OBJ.register_stream(r""" \
            | <test_oui> \
            | "coucou" \
            | :any: <coucou>
        """)
        node = CRUPY_DSL_PARSER_OBJ.execute('statement')
        self.assertEqual(node.type, 'dsl_statement')
        self.assertEqual(len(node.alternatives), 3)
        alts = node.alternatives
        self.assertEqual(alts[0].type, 'dsl_alternative')
        self.assertEqual(alts[1].type, 'dsl_alternative')
        self.assertEqual(alts[2].type, 'dsl_alternative')
        self.assertEqual(len(alts[0].seq), 1)
        self.assertEqual(len(alts[1].seq), 1)
        self.assertEqual(len(alts[2].seq), 2)
        self.assertEqual(alts[0].seq[0].type, 'dsl_production_name')
        self.assertEqual(alts[1].seq[0].type, 'dsl_string')
        self.assertEqual(alts[2].seq[0].type, 'dsl_builtin')
        self.assertEqual(alts[2].seq[1].type, 'dsl_production_name')

    ## error

    def test_error_broken_alternative(self) -> None:
        """ test error """
        CRUPY_DSL_PARSER_OBJ.register_stream('"yes no maybe')
        err = self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'statement'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 14\n'
                '"yes no maybe\n'
                '~~~~~~~~~~~~~^\n'
                'SyntaxError: missing enclosing quote',
        )
        self.assertEqual(err.reason, 'missing enclosing quote')
