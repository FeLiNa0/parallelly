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
                         Used in notifications and files storing output.
                         A cmd_with_arguments should always follow these args.
    cmd_with_arguments   An escaped command to run in parallel

Environment variables:
  Output:
    $PARALLELY_VERBOSE_OUTPUT:
        Whether to print verbose logs.
        If colors are enabled, logs are colored.
        Default: false or value of $VERBOSE if it is set
    $PARALLELY_EMOJI_OUTPUT:
        Whether to print emoji.
        Default: true if output is a tty and $DISPLAY is set, false otherwise.
    $ENABLE_COLORS: 
        If enabled, errors are colored.
        Default: true if output is a tty, false otherwise.
    $SHOW_FAILED_CMD_OUTPUT:
        Command for printing stderr and stdout of failed command/
        Default: tail -n1
        Example values:
          Show all output: cat
          Show last ten lines: tail -n10
          Show output for each command one at a time: less
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
        Should take one argument that contains spaces.
        Default: echo if $CLI_NOTIFY is false, GUI command otherwise.
    $FAILURE_NOTIFY_COMMAND:
        Command to notify when a command fails.
        Should take one argument.
        Default: echo if $CLI_NOTIFY is false, more visible GUI command otherwise.

Examples:

  Multiple commands:
    parallely fail 'echo failure && exit 1' \
      fail-printf-nonewline 'printf "%s %s"\ abc 123 ; false' \
      fail-rsync-src 'rsync -rhP nonexistentdir backup' \
      delay 'sleep 0.2' \
      fail-slower-delay '! sleep 0.4' \
      fail-no-output 'exit 210'

    The odd numbered arguments are short, filesafe names for each command.
    The names are used in notifications and files storing outout.

  A command without arguments:
    parallely list-files ls

  Verbose output and a command without arguments:
    VERBOSE=true parallely list-files ls
    PARALLELY_VERBOSE_OUTPUT=true parallely list-files ls

  A command with arguments:
    parallely rsync-src 'rsync -rhP src backup'

  A command with arguments that have spaces in them:
    parallely printf-abc 'printf "%s %s" abc 123'

  Shell commands:
    parallely test-exit 'echo failure && exit 1'
    parallely test-statement 'if true; then echo 1; fi'

    Commands are run in the sh shell with: sh -c "$COMMAND"

  Commands are waited one at a time in order:
    This means that you should list the fast commands first.
    VERBOSE=true parallely 1 'sleep 0.1' 2 'sleep 1' 3 'sleep 2'

    Or else, it'll take a bit longer to see successful outputs.
    VERBOSE=true parallely 3 'sleep 2' 2 'sleep 1' 1 'sleep 0.1'

    Regardless, you are notified as soon as a command finishes.
    VERBOSE=true CLI_NOTIFY=true parallely 3 'sleep 2' 2 'sleep 1' 1 'sleep 0.1'

Contributors: Hugo O. Rivera
Version: 1.4.0

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
