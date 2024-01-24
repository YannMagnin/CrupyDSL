"""
crupy.core.grammar.base     - base grammar class
"""
__all__ = [
    'CrupyGrammarBase',
]
from typing import Optional, Dict, Any, IO

from crupy.core.stream import CrupyStream
from crupy.core.grammar.exception import CrupyGrammarException
from crupy.core.grammar._dsl import (
    crupy_grammar_dsl_parse,
    crupy_grammar_dsl_compile,
)

#---
# Public
#---

class TestOui(Exception):
    """ aaa  """

class CrupyGrammarBase():
    """
    Most important class used to generate the parser using the special
    `production_entry` and `grammar` attribute
    """

    #---
    # Magic parser constructor
    #---

    grammar:            str
    production_entry:   Optional[str]
    _rules:             Dict[str,Any]

    def __init_subclass__(cls, /, **kwargs: Any) -> None:
        """ register the main base class
        """
        super().__init_subclass__(**kwargs)
        if not cls.grammar:
            raise CrupyGrammarException(
                'Missing the `grammar` class attribute in subclass '
                f"{cls.__name__}"
            )
        if not cls.production_entry:
            raise CrupyGrammarException(
                'Missing `production_entry` class attribute in subclass'
                f"{cls.__name__}"
            )
        crupy_grammar_dsl_parse(cls._rules, cls.grammar)

    #---
    # Public methods
    #---

    def parse(self, stream_origin: IO[str]|str) -> Any:
        """ parse the stream using the current grammar state
        """
        crupy_grammar_dsl_compile(self._rules)
        stream = CrupyStream.form_any(stream_origin)

    def grammar_add(self, grammar: str) -> None:
        """ aggregate the current grammar with an other piece of grammar
        """
