"""
tests.dsl.end_of_line   - test productions
"""
__all__ = [
    'CrupyUnittestDslEol',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

class CrupyUnittestDslEol(CrupyUnittestBase):
    """ unittest suite for the `eol` rules
    """

    #---
    # Public tests
    #---

    def test_simple_newline(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream('\n')
        node = CRUPY_DSL_PARSER_OBJ.execute('eol')
        self.assertEqual(node.type, 'dsl_eol')

    def test_complexe_newline(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream('\r\n')
        node = CRUPY_DSL_PARSER_OBJ.execute('eol')
        self.assertEqual(node.type, 'dsl_eol')

    def test_error(self) -> None:
        """ simple valid case """
        try:
            CRUPY_DSL_PARSER_OBJ.register_stream('prout')
            CRUPY_DSL_PARSER_OBJ.execute('eol')
            self.assertAlways('production eol has been executed')
        except CrupyParserBaseException as err:
            self.assertEqual(err.reason, 'not an end-of-file')
