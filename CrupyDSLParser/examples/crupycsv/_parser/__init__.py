"""
example.csv._parser - manually constructed parser object
"""
__all__ = [
    'CSV_PARSER_OBJ',
]

from crupydslparser.core.parser import CrupyParserBase
from crupydslparser.core._lexer import (
    CrupyLexerOpSeq,
    CrupyLexerOpText,
    CrupyLexerOpRep1N,
    CrupyLexerOpRep0N,
    CrupyLexerOpOr,
    CrupyLexerOpProductionCall,
    CrupyLexerAssertLookaheadNegative,
    CrupyLexerAssertEOF,
)

from crupycsv._parser.csv import csv_parser_prod_csv_hook
from crupycsv._parser.record import csv_parser_prod_record_hook
from crupycsv._parser.field import csv_parser_prod_field_hook

#---
# Public
#---

# the CSV grammar defined should generate the following parser object
# @note
# - the following hardcoded parser is used to validate the
# `CrupyParserBase` design
CSV_PARSER_OBJ = CrupyParserBase({
    #
    # production entry
    # > cvs ::= (<record> "\n")+ :eof:
    #
    'csv' : \
        CrupyLexerOpSeq(
            CrupyLexerOpRep1N(
                CrupyLexerOpSeq(
                    CrupyLexerOpProductionCall('record'),
                    CrupyLexerOpText('\n'),
                ),
            ),
            CrupyLexerAssertEOF(),
        ),

    #
    # CSV record
    # > record ::= <field> ("," <field>)*
    #
    'record' : \
        CrupyLexerOpSeq(
            CrupyLexerOpProductionCall('field'),
            CrupyLexerOpRep0N(
                CrupyLexerOpText(','),
                CrupyLexerOpProductionCall('field'),
            ),
        ),

    #
    # CSV field (simply nexus between quoted or sigle)
    # > field ::= <quoted_content> | <simple_content>
    #
    'field' : \
        CrupyLexerOpOr(
            CrupyLexerOpProductionCall('field_quoted'),
            CrupyLexerOpProductionCall('field_simple'),
        ),

    #
    # CSV quoted field
    # > quoted_field ::= \
    #       "\"" ((?!"\"")(<letter>|<digit>|<symbol>|<space>))+ "\""
    #
    'field_quoted' : \
        CrupyLexerOpSeq(
            CrupyLexerOpText('"'),
            CrupyLexerOpRep1N(
                CrupyLexerAssertLookaheadNegative(
                    CrupyLexerOpText('"'),
                ),
                CrupyLexerOpOr(
                    CrupyLexerOpProductionCall('letter'),
                    CrupyLexerOpProductionCall('digit'),
                    CrupyLexerOpProductionCall('symbol'),
                    CrupyLexerOpProductionCall('space'),
                ),
            ),
            CrupyLexerOpText('"'),
        ),

    #
    # CSV default field (capture between commad separator)
    # > simple_field ::= ((?!,)(<letter>|<digit>|<symbol>))*
    #
    'field_simple' : \
        CrupyLexerOpRep0N(
            CrupyLexerOpSeq(
                CrupyLexerAssertLookaheadNegative(
                    CrupyLexerOpText(','),
                ),
                CrupyLexerOpOr(
                    CrupyLexerOpProductionCall('letter'),
                    CrupyLexerOpProductionCall('digit'),
                    CrupyLexerOpProductionCall('symbol'),
                ),
            ),
        ),

    ## generic rules

    #
    # generic spaces
    #
    'space' : \
        CrupyLexerOpOr(
            CrupyLexerOpText(' '),
            CrupyLexerOpText('\t'),
            CrupyLexerOpText('\n'),
            CrupyLexerOpText('\v'),
        ),
    #
    # generic digits
    #
    'digit' : \
        CrupyLexerOpOr(
            CrupyLexerOpText('0'),
            CrupyLexerOpText('1'),
            CrupyLexerOpText('2'),
            CrupyLexerOpText('3'),
            CrupyLexerOpText('4'),
            CrupyLexerOpText('5'),
            CrupyLexerOpText('6'),
            CrupyLexerOpText('7'),
            CrupyLexerOpText('8'),
            CrupyLexerOpText('9'),
        ),
    #
    # generic symbol
    #
    'symbol' : \
        CrupyLexerOpOr(
            CrupyLexerOpText("|"),
            CrupyLexerOpText("~"),
            CrupyLexerOpText("!"),
            CrupyLexerOpText("#"),
            CrupyLexerOpText("$"),
            CrupyLexerOpText("%"),
            CrupyLexerOpText("&"),
            CrupyLexerOpText("("),
            CrupyLexerOpText(")"),
            CrupyLexerOpText("*"),
            CrupyLexerOpText("+"),
            CrupyLexerOpText(","),
            CrupyLexerOpText("-"),
            CrupyLexerOpText("."),
            CrupyLexerOpText("/"),
            CrupyLexerOpText(":"),
            CrupyLexerOpText(";"),
            CrupyLexerOpText(">"),
            CrupyLexerOpText("="),
            CrupyLexerOpText("<"),
            CrupyLexerOpText("?"),
            CrupyLexerOpText("@"),
            CrupyLexerOpText("["),
            CrupyLexerOpText("]"),
            CrupyLexerOpText("^"),
            CrupyLexerOpText("_"),
            CrupyLexerOpText("`"),
            CrupyLexerOpText("{"),
            CrupyLexerOpText("}"),
            CrupyLexerOpText("\\"),
            CrupyLexerOpText("\""),
        ),
    #
    # generic letter production
    #
    'letter' : \
        CrupyLexerOpOr(
            CrupyLexerOpText("A"),
            CrupyLexerOpText("B"),
            CrupyLexerOpText("C"),
            CrupyLexerOpText("D"),
            CrupyLexerOpText("E"),
            CrupyLexerOpText("F"),
            CrupyLexerOpText("G"),
            CrupyLexerOpText("H"),
            CrupyLexerOpText("I"),
            CrupyLexerOpText("J"),
            CrupyLexerOpText("K"),
            CrupyLexerOpText("L"),
            CrupyLexerOpText("M"),
            CrupyLexerOpText("N"),
            CrupyLexerOpText("O"),
            CrupyLexerOpText("P"),
            CrupyLexerOpText("Q"),
            CrupyLexerOpText("R"),
            CrupyLexerOpText("S"),
            CrupyLexerOpText("T"),
            CrupyLexerOpText("U"),
            CrupyLexerOpText("V"),
            CrupyLexerOpText("W"),
            CrupyLexerOpText("X"),
            CrupyLexerOpText("Y"),
            CrupyLexerOpText("Z"),
            CrupyLexerOpText("a"),
            CrupyLexerOpText("b"),
            CrupyLexerOpText("c"),
            CrupyLexerOpText("d"),
            CrupyLexerOpText("e"),
            CrupyLexerOpText("f"),
            CrupyLexerOpText("g"),
            CrupyLexerOpText("h"),
            CrupyLexerOpText("i"),
            CrupyLexerOpText("j"),
            CrupyLexerOpText("k"),
            CrupyLexerOpText("l"),
            CrupyLexerOpText("m"),
            CrupyLexerOpText("n"),
            CrupyLexerOpText("o"),
            CrupyLexerOpText("p"),
            CrupyLexerOpText("q"),
            CrupyLexerOpText("r"),
            CrupyLexerOpText("s"),
            CrupyLexerOpText("t"),
            CrupyLexerOpText("u"),
            CrupyLexerOpText("v"),
            CrupyLexerOpText("w"),
            CrupyLexerOpText("x"),
            CrupyLexerOpText("y"),
            CrupyLexerOpText("z"),
        ),
})

## register all hooks

CSV_PARSER_OBJ.register_hook('csv',    csv_parser_prod_csv_hook)
CSV_PARSER_OBJ.register_hook('record', csv_parser_prod_record_hook)
CSV_PARSER_OBJ.register_hook('field',  csv_parser_prod_field_hook)
