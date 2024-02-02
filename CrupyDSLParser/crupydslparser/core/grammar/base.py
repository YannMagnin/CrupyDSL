"""
crupydslparser.core.grammar.base     - base grammar class
"""
__all__ = [
    'CrupyGrammarBase',
]
from typing import Optional, Dict, Any, IO

from crupydslparser.core._stream import CrupyStream
from crupydslparser.core.grammar.exception import CrupyGrammarException
from crupydslparser.core._dsl import (
    crupy_dsl_parse,
    crupy_dsl_compile,
)

#---
# Public
#---

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
        crupy_dsl_parse(cls._rules, cls.grammar)

    #---
    # Public methods
    #---

    def parse(self, stream_origin: IO[str]|str) -> Any:
        """ parse the stream using the current grammar state
        """
        crupy_dsl_compile(self._rules)
        stream = CrupyStream.from_any(stream_origin)
        print(stream)

    def grammar_add(self, grammar: str) -> None:
        """ aggregate the current grammar with an other piece of grammar
        """
