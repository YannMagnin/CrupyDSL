"""
tests.dsl.space - test space productions
"""
__all__ = [
    'CrupyUnittestDslSpace',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydslparser.parser import CrupyParserBaseException

#---
# Public
#---

class CrupyUnittestDslSpace(CrupyUnittestBase):
    """ unittest suite for the `*space*` rules
    """

    #---
    # Public tests
    #---

    ## __space

    def test_space_lowlevel(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream(' \t \\\n')
        node1 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        node2 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        node3 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        node4 = CRUPY_DSL_PARSER_OBJ.execute('__space')
        self.assertEqual(node1.type, 'dsl_space')
        self.assertEqual(node2.type, 'dsl_space')
        self.assertEqual(node3.type, 'dsl_space')
        self.assertEqual(node4.type, 'dsl_space')

    def test_space_lowlevel_error(self) -> None:
        """ __space lowlevel error """
        try:
            CRUPY_DSL_PARSER_OBJ.register_stream('q\t \\\na')
            CRUPY_DSL_PARSER_OBJ.execute('__space')
            self.assertAlways('production __space has been executed')
        except CrupyParserBaseException as err:
            self.assertEqual(err.reason, 'not a space')

    ## space

    def test_space(self) -> None:
        """ space rule """
        CRUPY_DSL_PARSER_OBJ.register_stream(' \t \\\na')
        self.assertIsNotNone(CRUPY_DSL_PARSER_OBJ.execute('space'))
        with CRUPY_DSL_PARSER_OBJ.stream as context:
            self.assertEqual(context.read_char(), 'a')

    def test_space_error(self) -> None:
        """ space lowlevel error """
        try:
            CRUPY_DSL_PARSER_OBJ.register_stream('q\t \\\na')
            CRUPY_DSL_PARSER_OBJ.execute('space')
            self.assertAlways('production space has been executed')
        except CrupyParserBaseException as err:
            self.assertEqual(err.reason, 'missing at least one space')
