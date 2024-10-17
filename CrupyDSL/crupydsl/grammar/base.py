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
from crupydsl.grammar.exception import CrupyDSLGrammarBaseException
from crupydsl.grammar._dsl import (
    CRUPY_DSL_PARSER_OBJ,
    dsl_compil_grammar_node,
)
from crupydsl.parser import (
    CrupyDSLParserBase,
    CrupyDSLParserNodeBase,
)
from crupydsl.parser._lexer._operation.op_base import CrupyDSLLexerOpBase

#---
# Public
#---

@crupynamedclass(
    generate_type   = False,
    regex           = '^(_)*CrupyDSLGrammar(?P<type>([A-Z][a-z]+)+)$',
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
    production_entry:   Optional[str] = None

    def __init_subclass__(cls, /, **kwargs: Any) -> None:
        """ ensure that critical information are provided
        """
        super().__init_subclass__(**kwargs)
        if not cls.grammar:
            raise CrupyDSLGrammarBaseException(
                'Missing the `grammar` class attribute in subclass '
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
            assert prod.type == 'dsl_production'
            if prod.production_name in self._target_parser.production_book:
                raise CrupyDSLGrammarBaseException(
                    'unable to generate the production '
                    f"'{prod.production_name}': already defined"
                )
            operation = dsl_compil_grammar_node(prod.statement)
            if not isinstance(operation, CrupyDSLLexerOpBase):
                raise CrupyDSLGrammarBaseException(
                    'unable to generate the production '
                    f"'{prod.production_name}': cannot be a simple "
                    'assertion'
                )
            self._target_parser.production_book[
                prod.production_name
            ] = operation

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

    def parse(
        self,
        stream: Optional[Path|IO[str]|str] = None,
    ) -> CrupyDSLParserNodeBase:
        """ parse the stream using the current grammar state
        """
        if not self._production_entry:
            raise CrupyDSLGrammarBaseException('missing production entry')
        if stream:
            self._target_parser.register_stream(stream)
        return self._target_parser.execute(self._production_entry)

    def execute(
        self,
        production: str,
        stream: Optional[Path|IO[str]|str] = None,
    ) -> CrupyDSLParserNodeBase:
        """ try to execute a particular production
        """
        if stream:
            self._target_parser.register_stream(stream)
        return self._target_parser.execute(production)

    def register_stream(self, stream: Path|IO[str]|str) -> None:
        """ register a stream
        """
        self._target_parser.register_stream(stream)

    def grammar_update(self, grammar_shard: CrupyDSLGrammarBase) -> None:
        """ aggregate the current grammar with an other piece of grammar
        """
        self._grammar_update_core(grammar_shard)
        self._grammar_update_hook(grammar_shard)
