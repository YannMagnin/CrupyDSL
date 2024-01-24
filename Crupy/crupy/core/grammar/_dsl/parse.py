"""
crupy.core.grammar._dsl.parse   - DSL parser abstraction
"""
__all__ = [
    'crupy_grammar_dsl_parse',
]
from typing import Dict, Any

from crupy.core.stream import CrupyStream
from crupy.core.grammar._dsl._rules import CRUPY_DSL_RULES

#---
# Public
#---

def crupy_grammar_dsl_parse(rules: Dict[str,Any], grammar: str) -> None:
    """ parse a piece of DSL grammar and update rules
    """
    with CrupyStream.from_string(grammar) as stream:
        for rule in CRUPY_DSL_RULES['crupy_dls_rule'](stream):
            print(rule)
