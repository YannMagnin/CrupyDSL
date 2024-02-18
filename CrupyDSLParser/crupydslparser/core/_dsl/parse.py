"""
crupydslparser.core._dsl.parse   - DSL parser abstraction
"""
__all__ = [
    'crupy_dsl_parse',
]
from typing import Dict, Any

#from crupydslparser.core._stream import CrupyStream
#from crupydslparser.core._dsl._rules import CRUPY_DSL_RULES

#---
# Public
#---

def crupy_dsl_parse(rules: Dict[str,Any], grammar: str) -> None:
    """ parse a piece of DSL grammar and update rules
    """
    #with CrupyStream.from_string(grammar) as stream:
    #    for rule in CRUPY_DSL_RULES['crupy_dls_rule'](stream):
    #        print(rule)
    #print(rules)
