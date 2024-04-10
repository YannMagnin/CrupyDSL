"""
crupydslparser.grammar.base - base grammar class
"""
#__all__ = [
#    'CrupyGrammarBase',
#]
#from typing import Optional, Any, IO
#
#from crupydslparser.core._stream import CrupyStream
#from crupydslparser.core.grammar.exception import CrupyGrammarException
#
##---
## Public
##---
#
#class CrupyGrammarBase():
#    """
#    Most important class used to generate the parser using the special
#    `production_entry` and `grammar` attribute
#    """
#
#    #---
#    # Magic parser constructor
#    #---
#
#    grammar:            str
#    production_entry:   Optional[str]
#
#    def __init_subclass__(cls, /, **kwargs: Any) -> None:
#        """ register the main base class
#        """
#        super().__init_subclass__(**kwargs)
#        if not cls.grammar:
#            raise CrupyGrammarException(
#                'Missing the `grammar` class attribute in subclass '
#                f"{cls.__name__}"
#            )
#        if not cls.production_entry:
#            raise CrupyGrammarException(
#                'Missing `production_entry` class attribute in subclass'
#                f"{cls.__name__}"
#            )
#
#    def __init__(self) -> None:
#        #self._parser = CrupyGrammarParser()
#        #self._parser.dsl_compile(self.grammar)
#        pass
#
#    #---
#    # Public methods
#    #---
#
#    def parse(self, stream_origin: IO[str]|str) -> Any:
#        """ parse the stream using the current grammar state
#        """
#        stream = CrupyStream.from_any(stream_origin)
#        print(stream)
#
#    def grammar_add(self, grammar_shard: CrupyGrammarBase) -> None:
#        """ aggregate the current grammar with an other piece of grammar
#        """
#        # (todo) : check `grammar` class information
#        # (todo) : check "hooks" methods
#        #self._parser.dsl_compile(grammar_shard)
