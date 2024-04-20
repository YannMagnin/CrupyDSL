"""
tests.dsl.group - test group productions
"""
__all__ = [
    'CrupyUnittestDslGroup',
]

from crupydsltester.unittest import CrupyUnittestBase
from crupydslparser.grammar._dsl._parser import (
    CRUPY_DSL_PARSER_OBJ,
    CrupyDslParserException,
)
from crupydslparser.parser.exception import CrupyParserBaseException

#---
# Public
#---

class CrupyUnittestDslGroup(CrupyUnittestBase):
    """ unittest suite for the `*group*` rules
    """

    #---
    # Public tests
    #---

    ## success

    def test_simple(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream('(<test_oui>)')
        node = CRUPY_DSL_PARSER_OBJ.execute('group')
        self.assertEqual(node.type, 'dsl_group')
        self.assertIsNone(node.lookahead)
        self.assertIsNone(node.operation)
        self.assertEqual(node.statement.type, 'dsl_statement')
        self.assertEqual(len(node.statement.alternatives), 1)

    def test_simple_group(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream('(<test_oui> "non")')
        node = CRUPY_DSL_PARSER_OBJ.execute('group')
        self.assertEqual(node.type, 'dsl_group')
        self.assertIsNone(node.lookahead)
        self.assertIsNone(node.operation)
        self.assertEqual(node.statement.type, 'dsl_statement')
        self.assertEqual(len(node.statement.alternatives), 1)

    def test_group_lookahead_negative(self) -> None:
        """ lookahead tests """
        CRUPY_DSL_PARSER_OBJ.register_stream('(?!"oui")')
        node = CRUPY_DSL_PARSER_OBJ.execute('group')
        self.assertEqual(node.type, 'dsl_group')
        self.assertEqual(node.lookahead, 'negative')
        self.assertIsNone(node.operation)
        self.assertEqual(node.statement.type, 'dsl_statement')
        self.assertEqual(len(node.statement.alternatives), 1)

    def test_group_lookahead_positive(self) -> None:
        """ lookahead tests """
        CRUPY_DSL_PARSER_OBJ.register_stream('(?=<space_opt>)')
        node = CRUPY_DSL_PARSER_OBJ.execute('group')
        self.assertEqual(node.type, 'dsl_group')
        self.assertEqual(node.lookahead, 'positive')
        self.assertIsNone(node.operation)
        self.assertEqual(node.statement.type, 'dsl_statement')
        self.assertEqual(len(node.statement.alternatives), 1)

    def test_group_operation_zero_plus(self) -> None:
        """ operation zero plus """
        CRUPY_DSL_PARSER_OBJ.register_stream('(<space_opt> :any:)*')
        node = CRUPY_DSL_PARSER_OBJ.execute('group')
        self.assertEqual(node.type, 'dsl_group')
        self.assertIsNone(node.lookahead)
        self.assertEqual(node.operation, 'zero_plus')
        self.assertEqual(node.statement.type, 'dsl_statement')
        self.assertEqual(len(node.statement.alternatives), 1)

    def test_group_operation_one_plus(self) -> None:
        """ operation one plus """
        CRUPY_DSL_PARSER_OBJ.register_stream('(:any: | "2617")+')
        node = CRUPY_DSL_PARSER_OBJ.execute('group')
        self.assertEqual(node.type, 'dsl_group')
        self.assertIsNone(node.lookahead)
        self.assertEqual(node.operation, 'one_plus')
        self.assertEqual(node.statement.type, 'dsl_statement')
        self.assertEqual(len(node.statement.alternatives), 2)

    def test_group_operation_optional(self) -> None:
        """ operation optional """
        CRUPY_DSL_PARSER_OBJ.register_stream('(:any: | "2617" <rte>)?')
        node = CRUPY_DSL_PARSER_OBJ.execute('group')
        self.assertEqual(node.type, 'dsl_group')
        self.assertIsNone(node.lookahead)
        self.assertEqual(node.operation, 'optional')
        self.assertEqual(node.statement.type, 'dsl_statement')
        self.assertEqual(len(node.statement.alternatives), 2)

    ## error

    def test_error_start(self) -> None:
        """ error test """
        CRUPY_DSL_PARSER_OBJ.register_stream('oui_non)')
        err = self.assertRaises(
            cls_exc     = CrupyDslParserException,
            request     = (CRUPY_DSL_PARSER_OBJ, 'execute', 'group'),
            error       = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 1\n'
                'oui_non)\n'
                '^\n'
                'SyntaxError: missing opening parenthesis',
        )
        self.assertEqual(err.reason, 'missing opening parenthesis')

    def test_error_close(self) -> None:
        """ error test """
        CRUPY_DSL_PARSER_OBJ.register_stream('(:space:')
        err = self.assertRaises(
            cls_exc     = CrupyDslParserException,
            request     = (CRUPY_DSL_PARSER_OBJ, 'execute', 'group'),
            error       = \
                'DSL parsing exception occured:\n'
                '\n'
                'Stream: line 1, column 9\n'
                '(:space:\n'
                '~~~~~~~~^\n'
                'SyntaxError: missing enclosing parenthesis',
        )
        self.assertEqual(err.reason, 'missing enclosing parenthesis')

    # @note
    # > Since we use the CrupyLexerOpOptional() to fetch group operation,
    #   we cannot catch the CrupyLexerOpError() because it will be ignored
    #   by the optional behaviour
    #
    #def test_error_broken_operation(self) -> None:
    #    """ error test """
    #    try:
    #        CRUPY_DSL_PARSER_OBJ.register_stream('(:space:)&')
    #        CRUPY_DSL_PARSER_OBJ.execute('group')
    #        self.assertAlways('production group has been executed')
    #    except CrupyParserBaseException as err:
    #        self.assertEqual(
    #            err.reason,
    #            'broken group operation request that can only be '
    #            '"*", "+" or "?"',
    #        )
    #
    #def test_error_broken_assert(self) -> None:
    #    """ error test """
    #    try:
    #        CRUPY_DSL_PARSER_OBJ.register_stream('(?*')
    #        CRUPY_DSL_PARSER_OBJ.execute('group')
    #        self.assertAlways('production group has been executed')
    #    except CrupyParserBaseException as err:
    #        self.assertEqual(
    #            err.reason,
    #            'broken assertion request that can only be "?!" or "?="',
    #        )
