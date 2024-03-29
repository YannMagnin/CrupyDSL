"""
crupydslparser.core._dsl     - DSL abstraction
"""
__all__ = (
    'CrupyDSLException',
    'crupy_dsl_parse',
    'crupy_dsl_compile',
)
from crupydslparser.core._dsl.exception import CrupyDSLException
from crupydslparser.core._dsl.parse import crupy_dsl_parse
from crupydslparser.core._dsl.compile import crupy_dsl_compile
