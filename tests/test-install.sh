#!/bin/sh
COMMAND=parallely
if ! [ -f "$1/$COMMAND" ]; then
  echo Command "$COMMAND" not found in directory "$1"
  exit 1
fi

if ! command -v "$COMMAND" > /dev/null; then
    echo Command "$COMMAND" not found
    echo Check to make sure "$COMMAND" is in your PATH "$1"
    exit 1
fi

echo "$COMMAND -h > /dev/null"
if ! "$COMMAND" -h > /dev/null; then
    echo Command "$COMMAND" found, but failed to run
    exit 1
fi

echo Succesfully installed!
