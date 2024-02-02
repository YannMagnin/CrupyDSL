"""
crupydslparser.core._dsl.compile     - DSL compile abstraction
"""
__all__ = [
    'crupy_dsl_compile',
]
from typing import Dict, Any

#---
# Public
#---

def crupy_dsl_compile(rules: Dict[str,Any]) -> None:
    """ performs all rules link and check all rules integrity
    """
