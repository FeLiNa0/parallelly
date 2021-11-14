#!/bin/sh
echo You can show the configuration, the version, or debug information easily.
echo
echo BEGIN_CODE
set -x
parallely --show-configuration
parallely --no-emoji --light-mode --shell-command zsh --cc-args -n10 --show-configuration
parallely --version
parallely --debug
echo "$ parallely --trace  # Very noisy!"
