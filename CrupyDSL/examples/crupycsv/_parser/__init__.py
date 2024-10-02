"""
example.csv._parser - manually constructed parser object
"""
__all__ = [
    'CSV_PARSER_OBJ',
]

from crupydsl.parser import CrupyParserBase
from crupydsl.parser._lexer import (
    CrupyLexerOpSeq,
    CrupyLexerOpText,
    CrupyLexerOpRep1N,
    CrupyLexerOpRep0N,
    CrupyLexerOpOr,
    CrupyLexerOpProductionCall,
    CrupyLexerOpBuiltin,
    CrupyLexerOpBetween,
    CrupyLexerAssertLookaheadNegative,
)

from crupycsv._parser.prod_csv import csv_parser_prod_csv_hook
from crupycsv._parser.prod_record import csv_parser_prod_record_hook
from crupycsv._parser.prod_field import csv_parser_prod_field_hook

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
    # > cvs ::= (<record> :newline:)+ :eof:
    #
    'csv' : \
        CrupyLexerOpSeq(
            CrupyLexerOpRep1N(
                CrupyLexerOpSeq(
                    CrupyLexerOpProductionCall('record'),
                    CrupyLexerOpBuiltin('newline'),
                ),
            ),
            CrupyLexerOpBuiltin('eof'),
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
    # > quoted_field ::= '"'...'"'
    #
    'field_quoted' : \
        CrupyLexerOpBetween(
            startop         = CrupyLexerOpText('"'),
            endop           = CrupyLexerOpText('"'),
            with_newline    = False,
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
