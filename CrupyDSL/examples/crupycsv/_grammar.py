#"""
#crupycsv._grammar   - CSV grammar definition
#"""
#__all__ = [
#    'CrupyDSLGrammarCSV',
#]
#from crupydsl.grammar import CrupyDSLGrammarBase

#---
# Internals
#---

## high-level grammar definition

#class CrupyDSLGrammarCSV(CrupyDSLGrammarBase):
#    """ define CSV (ascii) grammar using Crupy DSL
#    """
#    production_entry    = 'csv'
#    grammar             = r"""
#        <csv>               ::= ( <record> "\n" )+
#        <record>            ::= <field> ( "," <field> )*
#        <field>             ::= <quoted_content> | <simple_content>
#        <simple_content>    ::= ((?!,)(<letter> | <digit> | <symbol>))*
#        <quoted_content>    ::= \
#                "\"" (:letter:|:digit:|:symbol:|:space:)+ "\""
#    """
