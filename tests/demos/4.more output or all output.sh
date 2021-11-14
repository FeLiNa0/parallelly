#!/bin/sh
export PARALLELY_TMP_DIR="/tmp/demo-tmp-dir"  # Deterministic output please
set -eu
echo To show more output, or all output use the \`--command-output-command or --c\`
echo and \`--command-output-command-args or --cc-args\` arguments.
echo You can use \`cat\` to show all output or \`tail -n10\` to show the last 10 lines.
echo
echo By default, only the last line of output is shown.
echo
echo BEGIN_CODE
set -x 
parallely -a onlylastline 'printf "a\nb\nc\nd\ne"'
echo
parallely --cc-args -n3 -a last3lines 'printf "a\nb\nc\nd\ne"'
echo
parallely --cc cat -a last3lines 'printf "a\nb\nc\nd\ne"'
