"""
crupydslparser.core._dsl.compile     - DSL compile abstraction
"""
__all__ = [
    'crupy_dsl_compile',
]
from typing import Any

#---
# Public
#---

def crupy_dsl_compile(rules: dict[str,Any]) -> None:
    """ performs all rules link and check all rules integrity
    """
