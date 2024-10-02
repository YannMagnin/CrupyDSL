"""
example.csv._parser - manually constructed parser object
"""
__all__ = [
    'CSV_PARSER_OBJ',
]

from crupydsl.parser import CrupyDSLParserBase
from crupydsl.parser._lexer import (
    CrupyDSLLexerOpSeq,
    CrupyDSLLexerOpText,
    CrupyDSLLexerOpRep1N,
    CrupyDSLLexerOpRep0N,
    CrupyDSLLexerOpOr,
    CrupyDSLLexerOpProductionCall,
    CrupyDSLLexerOpBuiltin,
    CrupyDSLLexerOpBetween,
    CrupyDSLLexerAssertLookaheadNegative,
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
# `CrupyDSLParserBase` design
CSV_PARSER_OBJ = CrupyDSLParserBase({
    #
    # production entry
    # > cvs ::= (<record> :newline:)+ :eof:
    #
    'csv' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpRep1N(
                CrupyDSLLexerOpSeq(
                    CrupyDSLLexerOpProductionCall('record'),
                    CrupyDSLLexerOpBuiltin('newline'),
                ),
            ),
            CrupyDSLLexerOpBuiltin('eof'),
        ),
    #
    # CSV record
    # > record ::= <field> ("," <field>)*
    #
    'record' : \
        CrupyDSLLexerOpSeq(
            CrupyDSLLexerOpProductionCall('field'),
            CrupyDSLLexerOpRep0N(
                CrupyDSLLexerOpText(','),
                CrupyDSLLexerOpProductionCall('field'),
            ),
        ),
    #
    # CSV field (simply nexus between quoted or sigle)
    # > field ::= <quoted_content> | <simple_content>
    #
    'field' : \
        CrupyDSLLexerOpOr(
            CrupyDSLLexerOpProductionCall('field_quoted'),
            CrupyDSLLexerOpProductionCall('field_simple'),
        ),
    #
    # CSV quoted field
    # > quoted_field ::= '"'...'"'
    #
    'field_quoted' : \
        CrupyDSLLexerOpBetween(
            startop         = CrupyDSLLexerOpText('"'),
            endop           = CrupyDSLLexerOpText('"'),
            with_newline    = False,
        ),
    #
    # CSV default field (capture between commad separator)
    # > simple_field ::= ((?!,)(<letter>|<digit>|<symbol>))*
    #
    'field_simple' : \
        CrupyDSLLexerOpRep0N(
            CrupyDSLLexerOpSeq(
                CrupyDSLLexerAssertLookaheadNegative(
                    CrupyDSLLexerOpText(','),
                ),
                CrupyDSLLexerOpOr(
                    CrupyDSLLexerOpBuiltin('alpha'),
                    CrupyDSLLexerOpBuiltin('digit'),
                    CrupyDSLLexerOpBuiltin('symbol'),
                ),
            ),
        ),
})

## register all hooks

CSV_PARSER_OBJ.register_post_hook('csv',    csv_parser_prod_csv_hook)
CSV_PARSER_OBJ.register_post_hook('record', csv_parser_prod_record_hook)
CSV_PARSER_OBJ.register_post_hook('field',  csv_parser_prod_field_hook)
