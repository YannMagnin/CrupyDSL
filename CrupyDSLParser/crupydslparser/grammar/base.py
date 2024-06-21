"""
crupydslparser.grammar.base - base grammar class
"""
# workaround to allow the use of partially defined class
from __future__ import annotations

__all__ = [
    'CrupyGrammarBase',
]
from typing import Optional, Any, IO

from crupydslparser.grammar.exception import CrupyGrammarException
from crupydslparser.grammar._dsl import (
    CRUPY_DSL_PARSER_OBJ,
    dsl_compil_grammar_statement,
)
from crupydslparser.parser import CrupyParserBase

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

    def __init_subclass__(cls, /, **kwargs: Any) -> None:
        """ ensure that critical information are provided
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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """ initialize grammar internal
        """
        super().__init__(*args, **kwargs)
        self._dsl_parser = CRUPY_DSL_PARSER_OBJ
        self._target_parser = CrupyParserBase()
        self._production_entry = self.production_entry
        self.grammar_update(self)

    def __str__(self) -> str:
        """ display the full grammar information
        """
        content  = ''
        content += self._target_parser.__str__()
        return content

    #---
    # Internal
    #---

    def _grammar_update_core(self, grammar: CrupyGrammarBase) -> None:
        """ add the defined grammar shard to the current grammar
        """
        self._dsl_parser.register_stream(grammar.grammar)
        node_tree = self._dsl_parser.execute('crupy_dsl')
        assert node_tree.type == 'dsl_entry'
        for prod in node_tree.productions:
            if prod.production_name in self._target_parser.production_book:
                raise CrupyGrammarException(
                    'unable to generate the production '
                    f"'{prod.production_name}': already defined"
                )
            self._target_parser.production_book[
                prod.production_name
            ] = dsl_compil_grammar_statement(prod.statement)

    def _grammar_update_hook(self, _grammar: CrupyGrammarBase) -> None:
        """ scan the grammar shard and check if there is production hook
        """
        print('todo : update grammar hook')

    #---
    # Public methods
    #---

    def parse(self, _stream_origin: IO[str]|str) -> Any:
        """ parse the stream using the current grammar state
        """
        print('todo : parse input stream')

    def grammar_update(self, grammar_shard: CrupyGrammarBase) -> None:
        """ aggregate the current grammar with an other piece of grammar
        """
        self._grammar_update_core(grammar_shard)
        self._grammar_update_hook(grammar_shard)
