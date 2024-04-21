"""
tests.dsl.production - test production productions
"""
__all__ = [
    'CrupyUnittestDslProduction',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydslparser.parser.exception import CrupyParserBaseException

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

    ## error

    def test_error_prodname(self) -> None:
        """ test error """
        CRUPY_DSL_PARSER_OBJ.register_stream('<entry ::= "allo?"')
        err = self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'production'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 7\n'
                '<entry ::= "allo?"\n'
                '~~~~~~^\n'
                'SyntaxError: missing enclosing chevron'
        )
        self.assertEqual(err.reason, 'missing enclosing chevron')

    def test_error_space0(self) -> None:
        """ test error """
        CRUPY_DSL_PARSER_OBJ.register_stream('<entry>::= "allo?"')
        err = self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'production'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 8\n'
                '<entry>::= "allo?"\n'
                '~~~~~~~^\n'
                'SyntaxError: missing space between production name and '
                'equal sign'
        )
        self.assertEqual(
            err.reason,
            'missing space between production name and equal sign',
        )

    def test_error_space1(self) -> None:
        """ test error """
        CRUPY_DSL_PARSER_OBJ.register_stream('<entry> ::="allo?"')
        err = self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'production'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 12\n'
                '<entry> ::="allo?"\n'
                '~~~~~~~~~~~^\n'
                'SyntaxError: missing space between equal sign and statement'
        )
        self.assertEqual(
            err.reason,
            'missing space between equal sign and statement',
        )

    def test_error_statement(self) -> None:
        """ test error """
        CRUPY_DSL_PARSER_OBJ.register_stream('<entry> ::= "allo?')
        err = self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'production'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 19\n'
                '<entry> ::= "allo?\n'
                '            ~~~~~~^\n'
                'SyntaxError: missing enclosing quote'
        )
        self.assertEqual(err.reason, 'missing enclosing quote')

    def test_error_eol(self) -> None:
        """ test error """
        CRUPY_DSL_PARSER_OBJ.register_stream('<entry> ::= "allo?" ::=')
        err = self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'production'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 20\n'
                '<entry> ::= "allo?" ::=\n'
                '~~~~~~~~~~~~~~~~~~~^\n'
                'SyntaxError: missing an end-of-line or and end-of-file '
                'to validate the production'
        )
        self.assertEqual(
            err.reason,
            'missing an end-of-line or and end-of-file to validate '
            'the production',
        )
