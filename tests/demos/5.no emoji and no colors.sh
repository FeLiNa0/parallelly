#!/bin/sh
set -eu
echo Parallelly prints emoji and colors when it seems they could be supported.
echo To turn them off, use \`--no-color\` and \`--no-emoji\`.
echo
echo BEGIN_CODE
set -x 
parallelly --no-color --no-emoji -a long-running 'echo OK >&2 && sleep 0.25' lots-of-output 'cat $(which parallelly)' failing 'echo ERROR ; exit 1'
