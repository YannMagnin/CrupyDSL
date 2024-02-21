"""
tests.lexer.dsl_production_name - test `crupy_dsl_production_name` rule
"""
__all__ = [
    'CrupyUnittestDSLProdName',
]

from crupydslparser.core.unittest import CrupyUnittestBase
from crupydslparser.core._dsl._parser import CRUPY_DSL_PARSER_OBJ
#---
# Public
#---

class CrupyUnittestDSLProdName(CrupyUnittestBase):
    """ unittest suite for the `crupy_dsl_production_name` rule
    """

    #---
    # Public tests
    #---

    def test_simple_success(self) -> None:
        """ simple valid case """
        CRUPY_DSL_PARSER_OBJ.register_stream('<oui_non>')
        node = CRUPY_DSL_PARSER_OBJ.execute('crupy_dsl_production_name')
        print(node)
