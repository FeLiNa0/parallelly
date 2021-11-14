#!/bin/sh
echo Use \`-V\` to show more detailed output.
echo It is helpful to use it in conjunction with \`-a\`.
echo
echo Notice that the files where output is being saved are printed as soon as the command is started.
echo "You can use \`tail -f <OUTPUT FILE>\` to see the output of a long-lived command."
echo
echo 'Look for "Starting " and "See output at:" near the top of the logs'
echo
echo BEGIN_CODE
set -x 
parallely -V -a long-running 'echo OK >&2 && sleep 0.25' lots-of-output 'cat $(which parallely)' failing 'echo ERROR ; exit 1'
