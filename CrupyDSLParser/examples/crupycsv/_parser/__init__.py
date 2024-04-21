"""
example.csv._parser - manually constructed parser object
"""
__all__ = [
    'CSV_PARSER_OBJ',
]

from crupydslparser.parser import CrupyParserBase
from crupydslparser.parser._lexer import (
    CrupyLexerOpSeq,
    CrupyLexerOpText,
    CrupyLexerOpRep1N,
    CrupyLexerOpRep0N,
    CrupyLexerOpOr,
    CrupyLexerOpProductionCall,
    CrupyLexerOpBuiltin,
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
                    CrupyLexerOpBuiltin('alpha'),
                    CrupyLexerOpBuiltin('digit'),
                    CrupyLexerOpBuiltin('symbol'),
                    CrupyLexerOpBuiltin('space_nl'),
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
                    CrupyLexerOpBuiltin('alpha'),
                    CrupyLexerOpBuiltin('digit'),
                    CrupyLexerOpBuiltin('symbol'),
                ),
            ),
        ),
})

## register all hooks

CSV_PARSER_OBJ.register_post_hook('csv',    csv_parser_prod_csv_hook)
CSV_PARSER_OBJ.register_post_hook('record', csv_parser_prod_record_hook)
CSV_PARSER_OBJ.register_post_hook('field',  csv_parser_prod_field_hook)
