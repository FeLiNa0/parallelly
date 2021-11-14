#!/bin/sh
echo Parallely runs multiple commands in parallel and captures their output.
echo You pass it pairs of arguments: a name for the command and the command itself.
echo
echo Failing command output is summarized with \`tail -n1\` and a list of
echo command names that failed is listed at the end.
echo By default, successful command output is not shown.
echo Timing information is shown for each command and for total runtime.
echo
echo Some of the commands that were run are indicated by a leading \`+ \`, such as \`+ tail -n1\` for showing output and the command itself.
echo
echo Notice that command output is save in a temporary directory.
echo
echo BEGIN_CODE
set -x
parallely long-running 'echo OK >&2 && sleep 0.25' lots-of-output 'cat $(which parallely)' failing 'echo ERROR ; exit 1'
