#!/usr/bin/env bash
#
# This script is used has a pre-commit hook to perform almost all of the
# checks that is performed in the github CI

# isolate the current working directory path and jump on it
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../" || exit 84

# workaround used to self-kill the current process if an error is detected
# in function
trap 'exit 1' TERM
export TOP_PID=$$

# helper for display and process shell command
checkcmd() {
  echo "-- " "$@"
  if ! ("$@" > /dev/null); then
    echo 'failed command, abord'
    kill -s TERM $TOP_PID
  fi
}

# check windows CRLF
# @notes
# We cannot use the `checkcmd` function because we use a pipe to grep special
# information
echo 'check windows CRLF'
echo '-- find . -not -type d -exec file "{}" ";"'
if (find . -not -type d -exec file "{}" ";" | grep CRLF)
then
  echo 'failed command, abord'
  kill -s TERM $TOP_PID
fi

# check codebase compliance
echo 'check the codebase'
checkcmd pylint -d R0903,R0801 CrupyDSL/crupydsl
checkcmd pylint -d R0903,R0801 CrupyDSL/examples/crupycsv
checkcmd pylint -d R0903,R0801 CrupyDSL/examples/crupyjson
checkcmd pylint -d R0903,R0801 CrupyDSL/tests

checkcmd mypy --strict CrupyDSL/crupydsl
checkcmd mypy --strict CrupyDSL/examples/crupycsv
checkcmd mypy --strict CrupyDSL/examples/crupyjson
checkcmd mypy --strict CrupyDSL/tests

checkcmd pyimportcheck CrupyDSL/crupydsl
checkcmd pyimportcheck CrupyDSL/examples/crupycsv
checkcmd pyimportcheck CrupyDSL/examples/crupyjson
# (todo) : pyimportcheck for tests/ but with without exported symbols

# check tests
echo 'check all unittest'
checkcmd crupycsv tests
checkcmd crupyjson tests
checkcmd pytest --tb=no
