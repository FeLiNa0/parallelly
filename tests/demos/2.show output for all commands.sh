#!/bin/sh
set -eu
echo Use \`-a\` to show output for successful commands as well.
echo
echo BEGIN_CODE
set -x
parallelly -a long-running 'echo OK >&2 && sleep 0.25' lots-of-output 'cat $(which parallelly)' failing 'echo ERROR ; exit 1'
