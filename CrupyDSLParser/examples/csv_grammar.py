"""
examples.csv_grammar    - define CSV grammar parser
"""

from crupydslparser.core.parser._base import CrupyParserBase
from crupydslparser.core.grammar import CrupyGrammarBase
from crupydslparser.core._lexer import (
    CrupyLexerSeq,
    CrupyLexerText,
    CrupyLexerRep1N,
    CrupyLexerRep0N,
    CrupyLexerOr,
    CrupyLexerProductionCall,
    CrupyLexerLookaheadNegative,
)

#---
# Internals
#---

## high-level grammar definition

class _CrupyGrammarCSV(CrupyGrammarBase):
    """ define CSV (ascii) grammar using Crupy DSL
    """
    production_entry    = 'csv'
    grammar             = r"""
        <csv>               ::= ( <record> "\n" )+
        <record>            ::= <field> ( "," <field> )*
        <field>             ::= <quoted_content> | <simple_content>
        <simple_content>    ::= ((?!,)(<letter> | <digit> | <symbol>))*
        <quoted_content>    ::= \
                "\"" (<letter>|<digit>|<symbol>|<space>)+ "\""

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

## low-level grammar definition

# the CSV grammar defined should generate the following parser object
# @note
# - the following hardcoded parser is used to validate the
# `CrupyParserBase` design
CSV_PARSER_CSV_OBJ = CrupyParserBase({
    #
    # production entry
    # > cvs ::= (<record> "\n")+
    #
    'csv' : \
        CrupyLexerRep1N(
            CrupyLexerSeq(
                CrupyLexerProductionCall('record'),
                CrupyLexerText('\n'),
            ),
        ),

    #
    # CSV record
    # > record ::= <field> ("," <field>)*
    #
    'record' : \
        CrupyLexerSeq(
            CrupyLexerProductionCall('field'),
            CrupyLexerRep0N(
                CrupyLexerText(','),
                CrupyLexerProductionCall('field'),
            ),
        ),

    #
    # CSV field (simply nexus between quoted or sigle)
    # > field ::= <quoted_content> | <simple_content>
    #
    'field' : \
        CrupyLexerOr(
            CrupyLexerProductionCall('quoted_filed'),
            CrupyLexerProductionCall('simple_filed'),
        ),

    #
    # CSV quoted field
    # > quoted_field ::= "\"" (<letter>|<digit>|<symbol>|<space>)+ "\""
    #
    'quoted_field' : \
        CrupyLexerSeq(
            CrupyLexerText('"'),
            CrupyLexerRep1N(
                CrupyLexerOr(
                    CrupyLexerProductionCall('letter'),
                    CrupyLexerProductionCall('digit'),
                    CrupyLexerProductionCall('symbol'),
                    CrupyLexerProductionCall('space'),
                ),
            ),
            CrupyLexerText('"'),
        ),

    #
    # CSV default field (capture between commad separator)
    # > simple_field ::= ((?!,)(<letter>|<digit>|<symbol>))*
    #
    'simple_field' : \
        CrupyLexerRep0N(
            CrupyLexerSeq(
                CrupyLexerLookaheadNegative(
                    CrupyLexerText(','),
                ),
                CrupyLexerOr(
                    CrupyLexerProductionCall('letter'),
                    CrupyLexerProductionCall('digit'),
                    CrupyLexerProductionCall('symbol'),
                ),
            ),
        ),

    ## generic rules

    #
    # generic spaces
    #
    'space' : \
        CrupyLexerOr(
            CrupyLexerText(' '),
            CrupyLexerText('\t'),
            CrupyLexerText('\n'),
            CrupyLexerText('\v'),
        ),

    #
    # generic digits
    #
    'digit' : \
        CrupyLexerOr(
            CrupyLexerText('0'),
            CrupyLexerText('1'),
            CrupyLexerText('2'),
            CrupyLexerText('3'),
            CrupyLexerText('4'),
            CrupyLexerText('5'),
            CrupyLexerText('6'),
            CrupyLexerText('7'),
            CrupyLexerText('8'),
            CrupyLexerText('9'),
        ),

    #
    # generic symbol
    #

    'symbol' : \
        CrupyLexerOr(
            CrupyLexerText("|"),
            CrupyLexerText("~"),
            CrupyLexerText("!"),
            CrupyLexerText("#"),
            CrupyLexerText("$"),
            CrupyLexerText("%"),
            CrupyLexerText("&"),
            CrupyLexerText("("),
            CrupyLexerText(")"),
            CrupyLexerText("*"),
            CrupyLexerText("+"),
            CrupyLexerText(","),
            CrupyLexerText("-"),
            CrupyLexerText("."),
            CrupyLexerText("/"),
            CrupyLexerText(":"),
            CrupyLexerText(";"),
            CrupyLexerText(">"),
            CrupyLexerText("="),
            CrupyLexerText("<"),
            CrupyLexerText("?"),
            CrupyLexerText("@"),
            CrupyLexerText("["),
            CrupyLexerText("]"),
            CrupyLexerText("^"),
            CrupyLexerText("_"),
            CrupyLexerText("`"),
            CrupyLexerText("{"),
            CrupyLexerText("}"),
            CrupyLexerText("\\"),
            CrupyLexerText("\""),
        ),

    #
    # generic letter production
    # > letter : [a-zA-Z]
    #
    'letter' : \
        CrupyLexerOr(
            CrupyLexerText("A"),
            CrupyLexerText("B"),
            CrupyLexerText("C"),
            CrupyLexerText("D"),
            CrupyLexerText("E"),
            CrupyLexerText("F"),
            CrupyLexerText("G"),
            CrupyLexerText("H"),
            CrupyLexerText("I"),
            CrupyLexerText("J"),
            CrupyLexerText("K"),
            CrupyLexerText("L"),
            CrupyLexerText("M"),
            CrupyLexerText("N"),
            CrupyLexerText("O"),
            CrupyLexerText("P"),
            CrupyLexerText("Q"),
            CrupyLexerText("R"),
            CrupyLexerText("S"),
            CrupyLexerText("T"),
            CrupyLexerText("U"),
            CrupyLexerText("V"),
            CrupyLexerText("W"),
            CrupyLexerText("X"),
            CrupyLexerText("Y"),
            CrupyLexerText("Z"),
            CrupyLexerText("a"),
            CrupyLexerText("b"),
            CrupyLexerText("c"),
            CrupyLexerText("d"),
            CrupyLexerText("e"),
            CrupyLexerText("f"),
            CrupyLexerText("g"),
            CrupyLexerText("h"),
            CrupyLexerText("i"),
            CrupyLexerText("j"),
            CrupyLexerText("k"),
            CrupyLexerText("l"),
            CrupyLexerText("m"),
            CrupyLexerText("n"),
            CrupyLexerText("o"),
            CrupyLexerText("p"),
            CrupyLexerText("q"),
            CrupyLexerText("r"),
            CrupyLexerText("s"),
            CrupyLexerText("t"),
            CrupyLexerText("u"),
            CrupyLexerText("v"),
            CrupyLexerText("w"),
            CrupyLexerText("x"),
            CrupyLexerText("y"),
            CrupyLexerText("z"),
        ),
})
