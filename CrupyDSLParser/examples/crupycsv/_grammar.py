"""
crupycsv._grammar   - CSV grammar definition
"""
__all__ = [
    'CrupyGrammarCSV',
]
from crupydslparser.core.grammar import CrupyGrammarBase

#---
# Internals
#---

## high-level grammar definition

class CrupyGrammarCSV(CrupyGrammarBase):
    """ define CSV (ascii) grammar using Crupy DSL
    """
    production_entry    = 'csv'
    grammar             = r"""
        <csv>               ::= ( <record> "\n" )+
        <record>            ::= <field> ( "," <field> )*
        <field>             ::= <quoted_content> | <simple_content>
        <simple_content>    ::= ((?!,)(<letter> | <digit> | <symbol>))*
        <quoted_content>    ::= \
                "\"" (<letter>|<digit>|<symbol>|:space:)+ "\""

        <letter> ::= \
              "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" \
            | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" \
            | "U" | "V" | "W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d" \
            | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" \
            | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" \
            | "y" | "z"
        <symbol> ::= \
              "|" | "~" | "!" | "#" | "$" | "%" | "&" | "(" | ")" | "*" \
            | "+" | "," | "-" | "." | "/" | ":" | ";" | ">" | "=" | "<" \
            | "?" | "@" | "[" | "\\"| "]" | "^" | "_" | "`" | "{" | "}"
        <digit>  ::= \
              "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
        <space>  ::= \
              " " | "\n"| "\t"| "\v"
    """
