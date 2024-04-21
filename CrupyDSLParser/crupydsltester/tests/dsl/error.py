"""
tests.dsl.error - test error productions
"""
__all__ = [
    'CrupyUnittestDslError',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.grammar._dsl._parser import CRUPY_DSL_PARSER_OBJ
from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

class CrupyUnittestDslError(CrupyUnittestBase):
    """ unittest suite for the `error` production
    """

    #---
    # Public tests
    #---

    ## fonctional

    def test_error(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream('@error("salut a tous")')
        node = CRUPY_DSL_PARSER_OBJ.execute('error')
        self.assertEqual(node.type, 'dsl_error')
        self.assertEqual(node.kind, 'error')
        self.assertEqual(node.error_name, 'salut a tous')

    def test_error_hook(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream('@error_hook("salut a tous")')
        node = CRUPY_DSL_PARSER_OBJ.execute('error')
        self.assertEqual(node.type, 'dsl_error')
        self.assertEqual(node.kind, 'hook')
        self.assertEqual(node.error_name, 'salut a tous')

    ## error

    def test_broken_start(self) -> None:
        """ error test  """
        CRUPY_DSL_PARSER_OBJ.register_stream('error("salut a tous")')
        err = self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'error'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 1\n'
                'error("salut a tous")\n'
                '^\n'
                'SyntaxError: manual error must start with "@"'
        )
        self.assertEqual(err.reason, 'manual error must start with "@"')

    def test_broken_kind(self) -> None:
        """ error test  """
        CRUPY_DSL_PARSER_OBJ.register_stream('@aaerror_foo("salut a tous")')
        err = self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'error'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 2\n'
                '@aaerror_foo("salut a tous")\n'
                '~^\n'
                'SyntaxError: only \'error\' and \'error_hook\' are '
                'currently supported'
        )
        self.assertEqual(
            err.reason,
            'only \'error\' and \'error_hook\' are currently supported'
        )

    def test_broken_openp(self) -> None:
        """ error test  """
        CRUPY_DSL_PARSER_OBJ.register_stream('@error"salut a tous")')
        err = self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'error'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 7\n'
                '@error"salut a tous")\n'
                '~~~~~~^\n'
                'SyntaxError: missing opening parenthesis'
        )
        self.assertEqual(err.reason, 'missing opening parenthesis')

    def test_broken_closep(self) -> None:
        """ error test  """
        CRUPY_DSL_PARSER_OBJ.register_stream('@error("salut a tous"')
        err = self.assertRaises(
            cls_exc = CrupyParserBaseException,
            request = (CRUPY_DSL_PARSER_OBJ, 'execute', 'error'),
            error   = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 22\n'
                '@error("salut a tous"\n'
                '~~~~~~~~~~~~~~~~~~~~~^\n'
                'SyntaxError: missing enclosing parenthesis'
        )
        self.assertEqual(err.reason, 'missing enclosing parenthesis')
