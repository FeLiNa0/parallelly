#!/usr/bin/env python3
"""Print given files, but replace <HELP_STRING> with `<command> -h`."""
import os.path
import re
import subprocess
from typing import List, Union
import sys


def log(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


def warn(*args, **kwargs):
    log("WARNING", *args, **kwargs)


HELP_MARKER = "<HELP_STRING>"
HELP_STRING_CMD = "parallely -h"

DEMO_MARKER = "<DEMO_OUTPUT>"
DEMO_DIRECTORY = "tests/demos/"
ACCEPTABLE_DEMO_EXIT_CODES = [0, 22]

PARALLELY_CMD_MARKER = "+ parallely"
PARALLELY_CMD_MARKER_REPLACEMENT = "$ parallely"

CWD = os.path.abspath(os.curdir)


def get_help(path: str) -> str:
    cmd = os.path.join(path, HELP_STRING_CMD).split()
    log(f"getting help string output")
    completed_process = subprocess.run(cmd, check=True, capture_output=True)
    return completed_process.stdout.decode("utf-8")


def wrap_command(output: List[str]) -> None:
    for i, line in enumerate(output):
        if line.startswith(PARALLELY_CMD_MARKER):
            output[i] = re.sub("' ", "' \\\n    ", line).replace(
                PARALLELY_CMD_MARKER, PARALLELY_CMD_MARKER_REPLACEMENT
            )


def string_or_int_sort_key(string: str) -> List[Union[str, int]]:
    return [int(word) if word.isdigit() else word for word in re.split("(\d+)", string)]


def get_demo_output() -> str:
    files = sorted(os.listdir(DEMO_DIRECTORY), key=string_or_int_sort_key)
    outputs = []
    for i, file in enumerate(files):
        log(f"getting demo #{1 + i}/{len(files)} output: {file}")
        filepath = os.path.join(DEMO_DIRECTORY, file)
        # send stderr to stdout
        completed_process = subprocess.run(
            ["/bin/bash", filepath],
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        )
        demo_name = re.sub("^\\d+\\.(.+).sh$", "\\1", file)
        outputs.append(f"\n### Demo {1 + i}: {demo_name}\n\n")
        output_str = completed_process.stdout.decode("utf-8")

        returncode = completed_process.returncode
        if returncode not in ACCEPTABLE_DEMO_EXIT_CODES:
            warn(
                f"Process status code {returncode} is not {' '.join(map(str, ACCEPTABLE_DEMO_EXIT_CODES))}! Output:",
                repr(output_str),
            )

        # Convert to lines
        output: List[str] = output_str.split("\n")

        # Wrap command
        wrap_command(output)

        found_code = False
        for i, line in enumerate(output):
            if "BEGIN_CODE" in line:
                output[i] = line.replace("BEGIN_CODE", "```")
                found_code = True

        if not found_code:
            warn(
                f"WARNING: string 'BEGIN_CODE' not found in output of demo file {filepath}",
                "output:\n",
                output,
            )
            outputs.append("```\n")
        outputs += output
        outputs.append("```")
    return "\n".join(outputs)


def main():
    if len(sys.argv) != 2:
        print(f"USAGE: {sys.argv[0]} [README_FILE]")
        sys.exit(1)

    fname = sys.argv[1]
    path = os.path.dirname(fname)

    help_string = get_help(path)
    demo_output = get_demo_output()

    with open(fname, "r", encoding="utf-8") as file:
        for line in file:
            print(
                line.replace(HELP_MARKER, help_string).replace(
                    DEMO_MARKER, demo_output
                ),
                end="",
            )


if __name__ == "__main__":
    main()
