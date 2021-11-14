#!/bin/sh
echo Parallely supports \`--sequential or -s\` to run commands sequentially instead of in parallel.
echo This is useful for testing and comparison purposes.
echo Also, you can use this mode to just capture output and notify on completion.
echo
echo BEGIN_CODE
set -x 
parallely --sequential -a long-running 'echo OK >&2 && sleep 0.25' lots-of-output 'cat $(which parallely)' failing 'echo ERROR ; exit 1'
