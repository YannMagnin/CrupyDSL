"""
tests.dsl.group - test group productions
"""
__all__ = [
    'CrupyUnittestDslGroup',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._dsl._parser import CRUPY_DSL_PARSER_OBJ

#---
# Public
#---

class CrupyUnittestDslGroup(CrupyUnittestBase):
    """ unittest suite for the `*group*` rules
    """

    #---
    # Public tests
    #---

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
