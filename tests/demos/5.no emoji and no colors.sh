#!/bin/sh
export PARALLELY_TMP_DIR="/tmp/demo-tmp-dir"  # Deterministic output please
set -eu
echo Parallely prints emoji and colors when it seems they could be supported.
echo To turn them off, use \`--no-color\` and \`--no-emoji\`.
echo
echo BEGIN_CODE
set -x 
parallely --no-color --no-emoji -a long-running 'echo OK >&2 && sleep 0.25' lots-of-output 'cat $(which parallely)' failing 'echo ERROR ; exit 1'
