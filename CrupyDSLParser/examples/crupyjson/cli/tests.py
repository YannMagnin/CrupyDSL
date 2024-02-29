"""
crupyjson.cli.tests     - JSON parser tests entry
"""
__all__ = [
    'crupyjson_cli_tests_entry',
]
from typing import NoReturn
import sys

import click

from crupyjson._parser import JSON_PARSER_OBJ
from crupyjson._tests._parser import (
    json_test_parser_nullable,
    json_test_parser_string,
    json_test_parser_boolean,
    json_test_parser_primitive,
    json_test_parser_array,
    json_test_parser_member,
    json_test_parser_object,
    json_test_parser_container,
    json_test_parser_statement,
    json_test_parser_json,
)

#---
# Public
#---

@click.command('tests')
def crupyjson_cli_tests_entry() -> NoReturn:
    """ run all tests """
    json_test_parser_nullable(JSON_PARSER_OBJ)
    json_test_parser_string(JSON_PARSER_OBJ)
    json_test_parser_boolean(JSON_PARSER_OBJ)
    json_test_parser_primitive(JSON_PARSER_OBJ)
    json_test_parser_array(JSON_PARSER_OBJ)
    json_test_parser_member(JSON_PARSER_OBJ)
    json_test_parser_object(JSON_PARSER_OBJ)
    json_test_parser_container(JSON_PARSER_OBJ)
    json_test_parser_statement(JSON_PARSER_OBJ)
    json_test_parser_json(JSON_PARSER_OBJ)
    sys.exit(0)
