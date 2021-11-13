# parallely: Run commands in parallel and capture output. Notify on each completion.

<!--
EDIT README.template.md, not README.md directly.
Use `make build-readme to update the README file
-->

## Usage

```
Description:
    Run commands in parallel and capture output. Notify on each completion.

    - Notify if a command succeeds (status code 0) or fails (non-zero status code).
    - Save command outputs to a temporary directory.
    - Print command output if the command fails.

    See examples in section below.

USAGE:
    parallely [-h|--help]
    parallely [cmd_name cmd_with_arguments]+

    One or more pairs of cmd_name followed by cmd_with_arguments are expected.

    --help|-h            Print this message.
    cmd_name             A short and filesafe name for the following command.
                         Used in notifications and files storing outout.
                         A cmd_with_arguments should always follow these args.
    cmd_with_arguments   An escaped command to run in parallel

Environment variables:
  Output:
    $PARALLELY_VERBOSE_OUTPUT:
        Whether to print verbose logs.
        If colors are enabled, logs are colored.
        Default: false or value of $VERBOSE if it is set
    $ENABLE_COLORS: 
        If enabled, errors are colored.
        Default: true if output is a tty, false otherwise.
    $SHOW_FAILED_CMD_OUTPUT:
        Command for printing stderr and stdout of failed command/
        Default: tail -n1
  Running commands:
    $CMD_SHELL:
        Which shell to run the commands in.
        Default: sh -c
  Notifications:
    $CLI_NOTIFY:
        Whether to use GUI to notify when a command finishes.
        Default: false if $DISPLAY is set, false otherwise.
    $NOTIFY_COMMAND:
        Command to notify when a command succeeds.
        Should take one argument.
        Default: echo if $CLI_NOTIFY is false, GUI command otherwise.
    $FAILURE_NOTIFY_COMMAND:
        Command to notify when a command fails.
        Should take one argument.
        Default: echo if $CLI_NOTIFY is false, more visible GUI command otherwise.

Examples:

  Multiple commands:
    parallely test-exit 'echo failure && exit 1' printf-abc 'printf "%s %s" abc 123' rsync-src 'rsync -rhP src backup'

    The odd numbered arguments are short, filesafe names for each command.
    The names are used in notifications and files storing outout.

  A command without arguments:
    parallely list-files ls

  Verbose output and a command without arguments:
    PARALLELY_VERBOSE_OUTPUT=true parallely list-files ls

  A command with arguments:
    parallely rsync-src 'rsync -rhP src backup'

  A command with arguments that have spaces in them:
    parallely printf-abc 'printf "%s %s" abc 123'

  Shell commands:
    parallely test-exit 'echo failure && exit 1'
    parallely test-statement 'if true; then echo 1; fi'

    Commands are run in the sh shell with: sh -c "$COMMAND"

Contributors: Hugo O. Rivera
Version: 1.2.2

```

## Installation

### Option 1:

1. Download [raw.githubusercontent.com/roguh/parallely/main/parallely](https://raw.githubusercontent.com/roguh/parallely/main/parallely).
2. Make executable and move to your preferred binary location.

```
chmod +x parallely
sudo cp parallely /usr/bin/parallely
```

### Option 2:

```
git clone https://github.com/roguh/parallely.git
cd parallely
make install
```

OR

```
git clone https://github.com/roguh/parallely.git
cd parallely
make install-to-user
```

OR

```
git clone https://github.com/roguh/parallely.git
cd parallely
make install-symlink-to-user
```

<!-- TODO
## Integration Testing

If the test script fails, the tests have failed.
Also read the output to determine if `parallely` is behaving correctly.

Note the `test-integration-all-shells.sh` script runs the `test-integration.sh` script using the test shell itself.

### Linux: Running tests for many shells at once

```
make test-on-linux
```

### MacOS: Running tests for many shells at once

```
make test-on-macos
```

### Running tests for stricter POSIX shells

```
make test-on-strict-posix-shells
```

### Running tests one shell at a time

Run the following commands:

```
./tests/test-integration.sh sh
./tests/test-integration.sh dash
./tests/test-integration.sh bash
BASH_COMPAT=31 ./tests/test-integration.sh bash
./tests/test-integration.sh zsh
```

### Test results

### Linux

Tested using GNU coreutils 9.0 in these shells:

- dash 0.5
- bash 5.1
- bash 5.1 in bash 3.1 compatibility mode BASH_COMPAT=31
- zsh 5.8
- yash 2.52
- ksh version 2020.0.0

### MacOS

Not tested on MacOS, yet. It should work fine.
-->

## Linting and Compatibility Check

Use shellcheck to check shellscripts.

```
make check
```
