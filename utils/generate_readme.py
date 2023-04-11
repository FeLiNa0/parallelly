#!/usr/bin/env python3
"""Print given files, but replace <HELP_STRING> with `<command> -h`."""
import asyncio
import shlex
import os.path
from os import environ
from hashlib import sha256
import re
import subprocess
from typing import List, Union, Tuple, Iterable, Dict, Coroutine, TypeVar
import sys


DEBUG = False
SCRIPT_NAME = "parallelly"
HELP_MARKER = "<HELP_STRING>"
HELP_STRING_CMD = f"{SCRIPT_NAME} -h"

EXEC_DEMOS_IN_PARALLEL = True

DEMO_MARKER = "<DEMO_OUTPUT>"
DEMO_DIRECTORY = "tests/demos/"
ACCEPTABLE_DEMO_EXIT_CODES = [0, 22]

SECONDS_MARKER = " seconds."
CMD_MARKER = f"+ {SCRIPT_NAME}"
PPID_MARKER = "PPID="

CWD = os.path.abspath(os.curdir)

BASE_DEMO_ENV = {
    # No user/date based strings in tmp dirs
    "TMP_DIR_SUFFIX": "",
    # No notifications
    # Only pass the $PATH
    "PATH": environ["PATH"],
    # For showing notifications with notify-send
    "DISPLAY": environ.get("DISPLAY", ""),
}

if BASE_DEMO_ENV["DISPLAY"] == "":
    BASE_DEMO_ENV |= {
        "NOTIFY_COMMAND": "true",
        "NOTIFY_COMMAND_ARGS": "",
        "FAILURE_NOTIFY_COMMAND": "true",
        "FAILURE_NOTIFY_COMMAND_ARGS": "",
    }


T = TypeVar("T")


def mk_env(demo_name_hash: str) -> Dict[str, str]:
    return BASE_DEMO_ENV | {
        # Deterministic tmp dir unique for every demo
        "PARALLELLY_TMP_DIR": f"/tmp/demo-tmp-dir-{demo_name_hash}",
    }


def log(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


def warn(*args, **kwargs):
    log("WARNING", *args, **kwargs)

def debug(*args, **kwargs):
    if DEBUG:
        log("DEBUG", *args, **kwargs)

def fail(*args, **kwargs):
    log("FAILURE", *args, **kwargs)
    sys.exit(1)


def get_help(path: str) -> str:
    cmd = os.path.join(path, HELP_STRING_CMD).split()
    log(f"getting help string output")
    completed_process = subprocess.run(cmd, check=True, capture_output=True)
    return completed_process.stdout.decode("utf-8")


def wrap_command(output: List[str]) -> None:
    for i, line in enumerate(output):
        if line.startswith(CMD_MARKER):
            new_line = line.replace(CMD_MARKER, f"$ {SCRIPT_NAME} \\\n   ")
            new_line = re.sub("' ", "' \\\n    ", new_line)
            output[i] = new_line


def round_seconds(output: List[str]) -> None:
    for i, line in enumerate(output):
        if line.endswith(SECONDS_MARKER):
            output[i] = re.sub(f"(\\d+\\.\\d)\\d+({SECONDS_MARKER})", "\\1\\2", line)


def elide_ppid(output: List[str]) -> None:
    for i, line in enumerate(output):
        if PPID_MARKER in line:
            output[i] = re.sub(
                f"{PPID_MARKER}.*",
                f"{PPID_MARKER}<omitted>",
                line,
            )


def string_or_int_sort_key(string: str) -> List[Union[str, int]]:
    return [
        int(word) if word.isdigit() else word for word in re.split("(\\d+)", string)
    ]


async def run_tasks(*async_tasks: Coroutine[None, None, T]) -> Iterable[T]:
    if EXEC_DEMOS_IN_PARALLEL:
        return await asyncio.gather(*async_tasks)
    results = []
    for task in async_tasks:
        results.append(await task)
    return results


async def get_demo_output(
    demo_index: int, demo_name: str, demo_hash: str, file: str
) -> Tuple[int, List[str]]:
    outputs = []
    filepath = os.path.join(DEMO_DIRECTORY, file)
    # send stderr to stdout
    proc = await asyncio.create_subprocess_shell(
        shlex.join(["/bin/bash", filepath]),
        stderr=asyncio.subprocess.STDOUT,
        stdout=asyncio.subprocess.PIPE,
        env=mk_env(demo_hash),
    )
    # Stderr is not needed as it is piped into stdout
    stdout, _ = await proc.communicate()

    log(f"Demo #{demo_index} finished: {file}")

    outputs.append(f"\n### Demo {demo_index}: {demo_name}\n\n")
    output_str = stdout.decode("utf-8")

    returncode = proc.returncode
    if returncode not in ACCEPTABLE_DEMO_EXIT_CODES:
        warn(
            f"Demo {demo_index} status code {returncode} is not {' or '.join(map(str, ACCEPTABLE_DEMO_EXIT_CODES))}! Output:",
            repr(output_str),
        )

    # Convert to lines
    output: List[str] = output_str.split("\n")

    wrap_command(output)
    round_seconds(output)
    elide_ppid(output)

    found_code = False
    for i, line in enumerate(output):
        if "BEGIN_CODE" in line:
            output[i] = line.replace("BEGIN_CODE", "```")
            found_code = True

    if not found_code:
        warn(
            f"String 'BEGIN_CODE' not found in output of demo file {filepath}",
            "output:\n",
            output,
        )
        outputs.append("```\n")
    outputs += output
    outputs.append("```")
    debug(outputs)
    return demo_index, outputs


async def get_all_demos_output() -> str:
    files = sorted(os.listdir(DEMO_DIRECTORY), key=string_or_int_sort_key)

    outputs = []
    demo_info = {}
    demo_hashes = set()
    tasks: List[Coroutine[None, None, Tuple[int, List[str]]]] = []
    for i, file in enumerate(files):
        demo_name = re.sub("^\\d+\\.(.+).sh$", "\\1", file)
        # Used for deterministic tmp dir names
        demo_hash = sha256(demo_name.encode("utf-8")).hexdigest()[:10]
        if demo_hash in demo_hashes:
            fail("Duplicate demo name hash! Cannot continue")
        else:
            demo_hashes.add(demo_hash)
        demo_info[i] = {
            "demo_name": demo_name,
            "demo_hash": demo_hash,
        }
    for i, file in enumerate(files):
        tasks.append(
            get_demo_output(
                i + 1, demo_info[i]["demo_name"], demo_info[i]["demo_hash"], file
            )
        )
    outputs = await run_tasks(*tasks)
    output = sum(
        [out for _, out in sorted(outputs, key=lambda ix_and_out: ix_and_out[0])],
        [],
    )
    return "\n".join(output)


def main():
    if len(sys.argv) != 2:
        print(f"USAGE: {sys.argv[0]} [README_FILE]")
        sys.exit(1)

    fname = sys.argv[1]
    path = os.path.dirname(fname)

    help_string = get_help(path)
    demo_output = asyncio.run(get_all_demos_output())

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
