#!/bin/sh
set -eu
echo You can show the configuration, the version, or debug information easily.
echo
echo BEGIN_CODE
echo "$ parallelly --trace  # Very noisy!"
set -x
parallelly --show-configuration
parallelly --no-emoji --light-mode --shell-command zsh --cc-args -n10 --show-configuration
parallelly --version
parallelly --debug
