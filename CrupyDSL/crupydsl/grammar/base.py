"""
crupydsl.grammar.base - base grammar class
"""
# workaround to allow the use of partially defined class
from __future__ import annotations

__all__ = [
    'CrupyDSLGrammarBase',
]
from typing import Optional, Any, IO
from pathlib import Path

from crupydsl._utils import crupynamedclass
from crupydsl.grammar.exception import CrupyDSLGrammarException
from crupydsl.grammar._dsl import (
    CRUPY_DSL_PARSER_OBJ,
    dsl_compil_grammar_statement,
)
from crupydsl.parser import (
    CrupyDSLParserBase,
    CrupyDSLParserNodeBase,
)

#---
# Public
#---

@crupynamedclass(
    generate_type   = False,
    regex           = '^(_)*CrupyDSLGrammar(?P<type>([A-Z][a-z]+)+)$',
    error           = 'malformated grammar subclass',
)
class CrupyDSLGrammarBase():
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
            raise CrupyDSLGrammarException(
                'Missing the `grammar` class attribute in subclass '
                f"{cls.__name__}"
            )
        if not cls.production_entry:
            raise CrupyDSLGrammarException(
                'Missing `production_entry` class attribute in subclass'
                f"{cls.__name__}"
            )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """ initialize grammar internal
        """
        super().__init__(*args, **kwargs)
        self._dsl_parser = CRUPY_DSL_PARSER_OBJ
        self._target_parser = CrupyDSLParserBase()
        self._production_entry = self.production_entry
        self.grammar_update(self)

    #---
    # Internal
    #---

    def _grammar_update_core(self, grammar: CrupyDSLGrammarBase) -> None:
        """ add the defined grammar shard to the current grammar
        """
        self._dsl_parser.register_stream(grammar.grammar)
        node_tree = self._dsl_parser.execute('crupy_dsl')
        assert node_tree.type == 'dsl_entry'
        for prod in node_tree.productions:
            if prod.production_name in self._target_parser.production_book:
                raise CrupyDSLGrammarException(
                    'unable to generate the production '
                    f"'{prod.production_name}': already defined"
                )
            self._target_parser.production_book[
                prod.production_name
            ] = dsl_compil_grammar_statement(prod.statement)

    def _grammar_update_hook(self, grammar: CrupyDSLGrammarBase) -> None:
        """ scan the grammar shard and check if there are production hook
        """
        for production in self._target_parser.production_book.keys():
            if hook := getattr(grammar, f"_{production}", None):
                self._target_parser.register_post_hook(production, hook)
            if hook := getattr(grammar, f"_{production}_error", None):
                self._target_parser.register_error_hook(production, hook)
    #---
    # Public methods
    #---

    def show(self) -> str:
        """ display the full grammar information
        """
        content  = ''
        content += self._target_parser.show()
        return content

    def parse(self, stream_origin: Path|IO[str]|str) -> CrupyDSLParserNodeBase:
        """ parse the stream using the current grammar state
        """
        if not self._production_entry:
            raise CrupyDSLGrammarException('missing production entry')
        stream_content: Any = stream_origin
        if isinstance(stream_origin, Path):
            if not stream_origin.exists():
                raise CrupyDSLGrammarException(
                    f"unable to find the file '{str(stream_origin)}'"
                )
            try:
                with open(stream_origin, 'r', encoding='utf-8') as stream_fd:
                    stream_content = stream_fd.read()
            except PermissionError as err:
                raise CrupyDSLGrammarException(
                    f"unable to open the file '{stream_origin}'"
                ) from err
        self._target_parser.register_stream(stream_content)
        return self._target_parser.execute(self._production_entry)

    def grammar_update(self, grammar_shard: CrupyDSLGrammarBase) -> None:
        """ aggregate the current grammar with an other piece of grammar
        """
        self._grammar_update_core(grammar_shard)
        self._grammar_update_hook(grammar_shard)
