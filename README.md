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
    - Measures total runtime.
    - Measures runtime of each command.

    See examples in section below.

USAGE:
    parallely -h|--help|-v|--version|<other options> [cmd_name cmd_with_arguments]+

    One or more pairs of cmd_name followed by cmd_with_arguments are expected.

    cmd_name             A short and filesafe name for the following command.
                         Used in notifications and files storing output.
                         A cmd_with_arguments should always follow these args.
    cmd_with_arguments   An escaped command to run in parallel

    -h|--help            Print this message.
    -v|--version         Print version of this script.

Configuration:
  Options take priority over environment variables.
  Options can go in between a name and its command.
  Use --show-configuration or --verbose to see configuration.

  Output configuration:
    --verbose|-V|--no-verbose or set $PARALLELY_VERBOSE_OUTPUT=true:
        Whether to print verbose logs.
        If colors are enabled, logs are colored.
        Default: false or value of $VERBOSE if it is set
    --all-output|-a|--not-all-output or set $PARALLELY_SHOW_ALL_OUTPUT=true:
        Whether to print command output for successful commands too.
        Default: false or value of $ALL_OUTPUT if it is set
    --emoji|-e|--no-emoji|-z or set $PARALLELY_EMOJI_OUTPUT=true:
        Whether to print emoji.
        Use --no-emoji if you see tofu characters (empty boxes), such as
        '' '' '�' '�'
        Default: true if output is a tty and $DISPLAY is set, false otherwise.
    --color|-c|--no-color|-n or set $ENABLE_COLORS=true: 
        If enabled, errors are colored.
        If enabled, verbose logs are colored.
        If enabled, some other logs are underemphasized.
          This color may not show up well on a light background.
          Use --light-mode in this case.
        Default: true if output is a tty and tput colors>=8, false otherwise.
          tput colors = 256
          is a tty = no
    --light-mode|--no-light-mode or set $LIGHT_MODE=true: 
    --command-output-command|--cc or set $SHOW_CMD_OUTPUT_CMD:
        Command for printing stderr and stdout of a command
        Default: tail
    --command-output-command-args|--cc-args  or set $SHOW_CMD_OUTPUT_CMD_ARG:
        Arguments for command for printing stderr and stdout of a command
        Default: -n1
  Running commands configuration:
    --sequential|-s|--no-sequential or set $FORCE_SEQUENTIAL=true:
        Run commands sequentially instead of in parallel.
        Useful if you just want to capture output and get notifications.
        Default: false
    --shell-command or set $CMD_SHELL:
        Which shell to run the commands in.
        Special value: RAW.
          Run the commands directly, without using a shell.
          Does not work on ZSH.
          Use only if you know what you're doing.
        Default: sh
    --shell-command-args or set $CMD_SHELL_ARGS:
        Arguments to pass to the shell
        Default: -c
  Notifications configuration:
    --notify-command or set $NOTIFY_COMMAND:
        Command to notify when a command succeeds.
        Should take two arguments, each possibly containing spaces.
        First argument is title, second is a description.
        Default: echo if $CLI_NOTIFY is false, GUI command otherwise.
    --failure-notify-command or set $FAILURE_NOTIFY_COMMAND:
        Command to notify when a command fails.
        Should take two arguments, each possibly containing spaces.
        First argument is title, second is a description.
        Default: echo if $CLI_NOTIFY is false, more visible GUI command otherwise.
    --notify-command-args or set $NOTIFY_COMMAND_ARGS
    --failure-notify-command-args or set $FAILURE_NOTIFY_COMMAND_ARGS

  Debug only:
    --show-configuration or set $SHOW_CONFIGURATION=true:
        Print configuration.
    --debug or set $DEBUG=true
    --trace or set $TRACE=true:
        Run 'set -x'

Exit codes:
    Exit code 0 is success.
    Exit code 2 indicates some or all commands failed.
    Other exit codes range from 51 to 90.
    See source code for an enumeration of all possible exit codes.

Examples:

  A command without arguments:
    parallely list-files ls

  Verbose output and a command without arguments:
    parallely -V list-files ls
    parallely list-files ls -V
    parallely list-files -V ls
    VERBOSE=true parallely list-files ls
    PARALLELY_VERBOSE_OUTPUT=true parallely list-files ls

  A command with arguments:
    parallely rsync-src 'rsync -rhP src backup'

  A command with arguments that have spaces in them:
    parallely printf-abc 'printf "%s %s" abc 123'

  Show more or all command output
    parallely multi-line-output --all-output --cc-args '-n5' 'echo 1; echo 2; echo 3; printf "%s %s" abc 123'
    parallely multi-line-output --all-output --cc cat --cc-args '' 'echo 1; echo 2; echo 3; printf "%s %s" abc 123'

  Shell commands:
    parallely test-exit 'echo failure && exit 1'
    parallely test-statement 'if true; then echo 1; fi'

    Commands are run in the sh by default shell with: sh -c "$COMMAND"

  Commands are waited one at a time in order:
    This means that you should list the fast commands first.
    VERBOSE=true parallely 1 'sleep 0.1' 2 'sleep 1' 3 'sleep 2'

    Or else, it'll take a bit longer to see successful outputs.
    VERBOSE=true parallely 3 'sleep 2' 2 'sleep 1' 1 'sleep 0.1'

    Regardless, you are notified as soon as a command finishes.
    VERBOSE=true CLI_NOTIFY=true parallely 3 'sleep 2' 2 'sleep 1' 1 'sleep 0.1'

  Multiple commands:
    parallely fail 'echo failure && exit 1' \
      fail-printf-nonewline 'printf "%s %s"\ abc 123 ; false' \
      fail-rsync-src 'rsync -rhP nonexistentdir backup' \
      delay 'sleep 0.2' \
      ok-and-output 'echo test ; echo stderr test >&2' \
      fail-slower-delay '! sleep 0.4' \
      fail-no-output 'exit 210' \
      'long name for command with spaces' 'true && echo ok'

    The odd numbered arguments are short, filesafe names for each command.
    The names are used in notifications and files storing outout.

Contributors: Hugo O. Rivera
Version: 1.8.1

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
-->

## Compatibility testing

### Linux

Tested on Manjaro using GNU coreutils 9.0 in these shells:

- dash 0.5
- bash 5.1
- bash 5.1 in bash 3.1 compatibility mode `BASH_COMPAT=31`
- zsh 5.8
- yash 2.52
- ksh version 2020.0.0

Tested in various shells:

- kitty 0.23.1
- xterm 369
- Termux terminal emulator 0.117

Tested on two OSs:

- Manjaro Linux (updated as of 2021.11)
- Termux 0.117 on Android 12

### MacOS

Not tested on MacOS, yet. It might work fine because it is tested on ZSH.
You will need to set the notify commands if you don't have `notify-send`.

## Linting and Compatibility Check

Use shellcheck to check shellscripts.

```
make check
```
