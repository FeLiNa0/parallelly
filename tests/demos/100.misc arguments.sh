#!/bin/sh
set -eu
echo You can show the configuration, the version, or debug information easily.
echo You can also disable emoji, set the shell used, e.g. to bash, zsh, or fish,
echo change the arguments passed to tail, and other options.
echo Use --help to see all options.
echo
echo BEGIN_CODE
echo "$ parallelly --trace  # Very noisy!"
set -x
parallelly --show-configuration
parallelly --no-emoji --light-mode --shell-command bash --cc tail --cc-args -n10 --show-configuration
parallelly --version
parallelly --debug
