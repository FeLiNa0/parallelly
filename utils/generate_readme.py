#!/usr/bin/env python3
"""Print given files, but replace <HELP_STRING> with `<command> -h`."""
import os.path
import subprocess
import sys

STR_TO_REPLACE = "<HELP_STRING>"
HELP_STRING_CMD = "parallely -h"


def main():
    if len(sys.argv) != 2:
        print(f"USAGE: {sys.argv[0]} [README_FILE]")
        sys.exit(1)

    fname = sys.argv[1]
    path = os.path.dirname(fname)

    cmd = os.path.join(path, HELP_STRING_CMD).split()
    completed_process = subprocess.run(cmd, check=True, capture_output=True)
    help_string = completed_process.stdout.decode("utf-8")

    with open(fname, "r", encoding="utf-8") as file:
        for line in file:
            print(line.replace(STR_TO_REPLACE, help_string), end="")


if __name__ == "__main__":
    main()
