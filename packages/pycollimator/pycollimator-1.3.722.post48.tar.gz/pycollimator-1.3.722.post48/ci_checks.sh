#!/bin/bash

set -e
cd `dirname $0`
source "env.sh"

do_echo "Running CI checks for collimator package in ENV=${ENV}..."

source venv/bin/activate
do_exec black --check .
do_exec pylint -E pycollimator
do_exec flake8 pycollimator

do_echo "Running pytest..."
do_exec bazel test //src/lib/pycollimator:all

do_echo "All good! You can now merge this PR."
