#!/bin/sh
export PARALLELY_TMP_DIR="/tmp/demo-tmp-dir"  # Deterministic output please
set -eu
echo You can show the configuration, the version, or debug information easily.
echo
echo BEGIN_CODE
echo "$ parallely --trace  # Very noisy!"
set -x
parallely --show-configuration
parallely --no-emoji --light-mode --shell-command zsh --cc-args -n10 --show-configuration
parallely --version
parallely --debug
