"""
tests.dsl.string_fix - test string productions
"""
__all__ = [
    'CrupyUnittestDslString',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

class CrupyUnittestDslString(CrupyUnittestBase):
    """ unittest suite for the `*string*` rules
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream(r'"667 oui ~# \\ dslk"')
        node = CRUPY_DSL_PARSER_OBJ.execute('string')
        self.assertEqual(node.type, 'dsl_string')
        self.assertEqual(node.text, r'667 oui ~# \ dslk')

    def test_escape(self) -> None:
        """ test escaping """
        CRUPY_DSL_PARSER_OBJ.register_stream('"\\"\\\\"')
        node = CRUPY_DSL_PARSER_OBJ.execute('string')
        self.assertEqual(node.type, 'dsl_string')
        self.assertEqual(node.text, '"\\')

    def test_error_enclose(self) -> None:
        """ test error handling """
        CRUPY_DSL_PARSER_OBJ.register_stream('"allo?')
        self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'string'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 7\n'
                '"allo?\n'
                '~~~~~~^\n'
                '\n'
                'SyntaxError: missing enclosing quote'
        )

    def test_error_open(self) -> None:
        """ test error handling """
        CRUPY_DSL_PARSER_OBJ.register_stream('allo?"')
        self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'string'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 1\n'
                'allo?"\n'
                '^\n'
                '\n'
                'SyntaxError: missing starting quote'
        )
