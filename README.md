# parallelly: Run commands in parallel and capture output. Notify on each completion.

<!--
EDIT README.template.md, not README.md directly.
Use `make build-readme to update the README file
-->

Add synchronized swimming to your CLI!

## Usage

See [demos at bottom of document](#demos) for examples with output.

```
Description:
    Run commands in parallel and capture output. Notify on each completion.

    - Notify if a command succeeds (status code 0) or fails (non-zero status code).
    - Save command outputs to a temporary directory.
    - Print command output if the command fails.
    - (Optional) Print command output if the command succeeds.
    - Print line count of command output.
    - Measures total runtime.
    - Measures runtime of each command.

    See examples in section below.

USAGE:
    parallelly -h|--help|-v|--version|<other options> [cmd_name cmd_with_arguments]+

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
    --verbose|-V|--no-verbose or set $PARALLELLY_VERBOSE_OUTPUT=true:
        Whether to print verbose logs.
        If colors are enabled, logs are colored.
        Default: false or value of $VERBOSE if it is set
    --all-output|-a|--not-all-output or set $PARALLELLY_SHOW_ALL_OUTPUT=true:
        Whether to print command output for successful commands too.
        Default: false or value of $ALL_OUTPUT if it is set
    --emoji|-e|--no-emoji|-z or set $PARALLELLY_EMOJI_OUTPUT=true:
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
        Default: true only if
            - output is a tty and tput colors>=8, false otherwise.
            - tput is installed
            - tput colors>=8
          tput colors = 8
          is a tty = no
    --light-mode|--no-light-mode or set $LIGHT_MODE=true: 
    --command-output-command|--cc or set $SHOW_CMD_OUTPUT_CMD:
        Command for printing stderr and stdout of a command
        If this argument is passed, --cc-args is set to '' by default.
        Make sure to pass --cc-args AFTER this argument.
        Default: tail
    --command-output-command-args|--cc-args or set $SHOW_CMD_OUTPUT_CMD_ARGS:
        Arguments for command for printing stderr and stdout of a command
        Default: -n1
    --tmp-dir or set $PARALLELLY_TMP_DIR:
        If you don't have mktemp on your system, you must set this
        option with the environment variable!
        Note: parallelly usually needs a tmp directory to parse its arguments!
        Alternative: set $MK_TEMP and $MK_TEMP_ARGS
        Default: created using mktemp
    --line-count|--no-line-count or set $SHOW_LINE_COUNT:
        Whether to show line count.
        Default: true
    --byte-count|--no-byte-count or set $SHOW_BYTE_COUNT:
        Whether to show byte count.
        Default: true
    --human-readable-byte-count|-H|--raw-byte-count or set $HUMAN_READABLE_BYTE_COUNT:
        Whether to show byte count in binary prefixes, such as 10MiB.
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
    --show-pids or set $SHOW_PIDS=true:
        Print process IDs of background jobs.
        Incompatible with --sequential.
    --debug or set $DEBUG=true
    --trace or set $TRACE=true:
        Run 'set -x'

Exit codes:
    Exit code 0 is success.
    Exit code 22 indicates some or all commands failed.
    Other exit codes range from 55 to 99.
    See source code for an enumeration of all possible exit codes.

Examples:

  A command without arguments:
    parallelly list-files ls

  Verbose output and a command without arguments:
    parallelly -V list-files ls
    parallelly list-files ls -V
    parallelly list-files -V ls
    VERBOSE=true parallelly list-files ls
    PARALLELLY_VERBOSE_OUTPUT=true parallelly list-files ls

  A command with arguments:
    parallelly rsync-src 'rsync -rhP src backup'

  A command with arguments that have spaces in them:
    parallelly printf-abc 'printf "%s %s" abc 123'

  Show more or all command output
    parallelly multi-line-output --all-output --cc-args '-n5' 'echo 1; echo 2; echo 3; printf "%s %s" abc 123'
    parallelly multi-line-output --all-output --cc cat --cc-args '' 'echo 1; echo 2; echo 3; printf "%s %s" abc 123'

  Shell commands:
    parallelly test-exit 'echo failure && exit 1'
    parallelly test-statement 'if true; then echo 1; fi'

    Commands are run in the sh by default shell with: sh -c "$COMMAND"

  Commands are waited one at a time in order:
    This means that you should list the fast commands first.
    VERBOSE=true parallelly 1 'sleep 0.1' 2 'sleep 1' 3 'sleep 2'

    Or else, it'll take a bit longer to see successful outputs.
    VERBOSE=true parallelly 3 'sleep 2' 2 'sleep 1' 1 'sleep 0.1'

    Regardless, you are notified as soon as a command finishes.
    VERBOSE=true CLI_NOTIFY=true parallelly 3 'sleep 2' 2 'sleep 1' 1 'sleep 0.1'

  Multiple commands:
    parallelly fail 'echo failure && exit 1' \
      fail-printf-nonewline 'printf "%s %s"\ abc 123 ; false' \
      fail-rsync-src 'rsync -rhP nonexistentdir backup' \
      delay 'sleep 0.2' \
      ok-and-output 'echo test ; echo stderr test >&2' \
      fail-slower-delay '! sleep 0.4' \
      fail-no-output 'exit 210' \
      lots-of-output 'cat $(which parallelly)' \
      'long name for command with spaces' 'true && echo ok'

    The odd numbered arguments are short, filesafe names for each command.
    The names are used in notifications and files storing outout.

Add synchronized swimming to your CLI!
Version: 1.11.2

```

## Installation

### Option 1:

1. Download [raw.githubusercontent.com/roguh/parallelly/main/parallelly](https://raw.githubusercontent.com/roguh/parallelly/main/parallelly).
2. Make executable and move to your preferred binary location.

```
chmod +x parallelly
sudo cp parallelly /usr/bin/parallelly
```

### Option 2:

```
git clone https://github.com/roguh/parallelly.git
cd parallelly
make install
```

OR

```
git clone https://github.com/roguh/parallelly.git
cd parallelly
make install-to-user
```

OR

```
git clone https://github.com/roguh/parallelly.git
cd parallelly
make install-symlink-to-user
```

## Tests

Run `make build-readme` to run various tests.

Output will be found in generated README.md file.

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

## Demos

The parallelly commands start with a `$ ` to indicate it is a command typed into the shell.
The rest of the code is the output of the command.


### Demo 1: basic usage


Parallelly runs multiple commands in parallel and captures their output.
You pass it pairs of arguments: a name for the command and the command itself.

Failing command output is summarized with `tail -n1` and a list of
command names that failed is listed at the end.
By default, successful command output is not shown.
Timing information is shown for each command and for total runtime.

Some of the commands that were run are indicated by a leading `+ `, such as `+ tail -n1` for showing output and the command itself.

Notice that command output is save in a temporary directory.

```
$ parallelly \
    long-running 'echo OK >&2 && sleep 0.25' \
    lots-of-output 'cat $(which parallelly)' \
    failing 'echo ERROR ; exit 1'
parallelly will run 3 commands in parallel 
============= Failed command output =============
ERROR Failure in command failing after 0.0 seconds.
+ echo ERROR ; exit 1
/tmp/demo-tmp-dir-24e84ee24f/parallelly-logs/failing.stderr
/tmp/demo-tmp-dir-24e84ee24f/parallelly-logs/failing.stdout
STDERR output for failed command failing: (no output)
STDOUT output for failed command failing: 6 bytes 1 line
+ tail -n1 /tmp/demo-tmp-dir-24e84ee24f/parallelly-logs/failing.stdout
ERROR
3 commands finished in 0.6 seconds.
ERROR 1 command failed: failing 

```

### Demo 2: speedup demo


Here, we're going to run ten sleep 0.1 commands in parallel and then sequentially to compare the runtime.

```
$ parallelly \
    sleep1 'sleep 0.1' \
    sleep2 'sleep 0.1' \
    sleep3 'sleep 0.1' \
    sleep4 'sleep 0.1' \
    sleep5 'sleep 0.1' \
    sleep6 'sleep 0.1' \
    sleep7 'sleep 0.1' \
    sleep8 'sleep 0.1' \
    sleep9 'sleep 0.1' \
    sleep0 'sleep 0.1'
parallelly will run 10 commands in parallel 
10 commands finished in 0.5 seconds.
+ echo

$ parallelly \
    --sequential sleep1 'sleep 0.1' \
    sleep2 'sleep 0.1' \
    sleep3 'sleep 0.1' \
    sleep4 'sleep 0.1' \
    sleep5 'sleep 0.1' \
    sleep6 'sleep 0.1' \
    sleep7 'sleep 0.1' \
    sleep8 'sleep 0.1' \
    sleep9 'sleep 0.1' \
    sleep0 'sleep 0.1'
parallelly will run 10 commands sequentially 
FORCE_SEQUENTIAL is set: Waiting for command sleep1 to finish
FORCE_SEQUENTIAL is set: Waiting for command sleep2 to finish
FORCE_SEQUENTIAL is set: Waiting for command sleep3 to finish
FORCE_SEQUENTIAL is set: Waiting for command sleep4 to finish
FORCE_SEQUENTIAL is set: Waiting for command sleep5 to finish
FORCE_SEQUENTIAL is set: Waiting for command sleep6 to finish
FORCE_SEQUENTIAL is set: Waiting for command sleep7 to finish
FORCE_SEQUENTIAL is set: Waiting for command sleep8 to finish
FORCE_SEQUENTIAL is set: Waiting for command sleep9 to finish
FORCE_SEQUENTIAL is set: Waiting for command sleep0 to finish
10 commands finished in 1.3 seconds.

```

### Demo 3: show output for all commands


Use `-a` to show output for successful commands as well.

```
$ parallelly \
    -a long-running 'echo OK >&2 && sleep 0.25' \
    lots-of-output 'cat $(which parallelly)' \
    failing 'echo ERROR ; exit 1'
parallelly will run 3 commands in parallel 
============= Successful command(s) =============
Command long-running succeeded in 0.2 seconds.
+ echo OK >&2 && sleep 0.25
/tmp/demo-tmp-dir-ca128f1014/parallelly-logs/long-running.stderr
/tmp/demo-tmp-dir-ca128f1014/parallelly-logs/long-running.stdout
STDERR output for successful command long-running: 3 bytes 1 line
+ tail -n1 /tmp/demo-tmp-dir-ca128f1014/parallelly-logs/long-running.stderr
OK
STDOUT output for successful command long-running: (no output)

Command lots-of-output succeeded in 0.0 seconds.
+ cat $(which parallelly)
/tmp/demo-tmp-dir-ca128f1014/parallelly-logs/lots-of-output.stderr
/tmp/demo-tmp-dir-ca128f1014/parallelly-logs/lots-of-output.stdout
STDERR output for successful command lots-of-output: (no output)
STDOUT output for successful command lots-of-output: 36.84 KiBs 1162 lines
+ tail -n1 /tmp/demo-tmp-dir-ca128f1014/parallelly-logs/lots-of-output.stdout
# End of parallelly script

============= Failed command output =============
ERROR Failure in command failing after 0.0 seconds.
+ echo ERROR ; exit 1
/tmp/demo-tmp-dir-ca128f1014/parallelly-logs/failing.stderr
/tmp/demo-tmp-dir-ca128f1014/parallelly-logs/failing.stdout
STDERR output for failed command failing: (no output)
STDOUT output for failed command failing: 6 bytes 1 line
+ tail -n1 /tmp/demo-tmp-dir-ca128f1014/parallelly-logs/failing.stdout
ERROR
3 commands finished in 0.8 seconds.
ERROR 1 command failed: failing 

```

### Demo 4: verbose mode for even more output


Use `-V` to show more detailed output.
It is helpful to use it in conjunction with `-a`.

Notice that the files where output is being saved are printed as soon as the command is started.
You can use `tail -f <OUTPUT FILE>` to see the output of a long-lived command.

Look for "Starting " and "See output at:" near the top of the logs

```
$ parallelly \
    -V -a long-running 'echo OK >&2 && sleep 0.25' \
    lots-of-output 'cat $(which parallelly)' \
    failing 'echo ERROR ; exit 1'
Created tmp directory at /tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs
============= Configuration =============
Environment variables may have been overridden by command line options.

PARALLELLY_VERBOSE_OUTPUT=true
PARALLELLY_SHOW_ALL_OUTPUT=true
PARALLELLY_EMOJI_OUTPUT=false
CMD_SHELL=sh
CMD_SHELL_ARGS=-c
FORCE_SEQUENTIAL=false
SHOW_CMD_OUTPUT_CMD=tail
SHOW_CMD_OUTPUT_CMD_ARGS=-n1
PARALLELLY_TMP_DIR=/tmp/demo-tmp-dir-86b09d2f5f
SHOW_LINE_COUNT=true
SHOW_BYTE_COUNT=true
HUMAN_READABLE_BYTE_COUNT=true
NOTIFY_COMMAND=true
FAILURE_NOTIFY_COMMAND=true
NOTIFY_COMMAND_ARGS=
FAILURE_NOTIFY_COMMAND_ARGS=
ENABLE_COLORS=false
LIGHT_MODE=false
SHOW_CONFIGURATION=false
SHOW_PIDS=false
Temporary directory CMD_OUT_DIR=/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs

parallelly will run 3 commands in parallel 
============= Starting commands =============
Starting long-running command 1/3
+ sh -c echo OK >&2 && sleep 0.25
See output at:
/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/long-running.stderr
/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/long-running.stdout
Starting lots-of-output command 2/3
+ sh -c cat $(which parallelly)
See output at:
/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/lots-of-output.stderr
/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/lots-of-output.stdout
Starting failing command 3/3
+ sh -c echo ERROR ; exit 1
See output at:
/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/failing.stderr
/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/failing.stdout

============= Waiting for commands to finish =============
Will list successful and failed commands.

============= Successful command(s) =============
Command long-running succeeded in 0.2 seconds.
+ echo OK >&2 && sleep 0.25
/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/long-running.stderr
/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/long-running.stdout
STDERR output for successful command long-running: 3 bytes 1 line
+ tail -n1 /tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/long-running.stderr
OK
STDOUT output for successful command long-running: (no output)

Command lots-of-output succeeded in 0.0 seconds.
+ cat $(which parallelly)
/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/lots-of-output.stderr
/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/lots-of-output.stdout
STDERR output for successful command lots-of-output: (no output)
STDOUT output for successful command lots-of-output: 36.84 KiBs 1162 lines
+ tail -n1 /tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/lots-of-output.stdout
# End of parallelly script

============= Failed command output =============
ERROR Failure in command failing after 0.0 seconds.
+ echo ERROR ; exit 1
/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/failing.stderr
/tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/failing.stdout
STDERR output for failed command failing: (no output)
STDOUT output for failed command failing: 6 bytes 1 line
+ tail -n1 /tmp/demo-tmp-dir-86b09d2f5f/parallelly-logs/failing.stdout
ERROR

============= SUMMARY =============
2 commands succeeded
3 commands finished in 0.8 seconds.
ERROR 1 command failed: failing 

```

### Demo 5: more output or all output


To show more output, or all output use the `--command-output-command or --c`
and `--command-output-command-args or --cc-args` arguments.
You can use `cat` to show all output or `tail -n10` to show the last 10 lines.

By default, only the last line of output is shown.

```
$ parallelly \
    -a onlylastline 'printf "a\nb\nc\nd\ne"'
parallelly will run 1 commands in parallel 
============= Successful command(s) =============
Command onlylastline succeeded in 0.0 seconds.
+ printf "a\nb\nc\nd\ne"
/tmp/demo-tmp-dir-71ab5eeb4a/parallelly-logs/onlylastline.stderr
/tmp/demo-tmp-dir-71ab5eeb4a/parallelly-logs/onlylastline.stdout
STDERR output for successful command onlylastline: (no output)
STDOUT output for successful command onlylastline: 9 bytes 4 lines
+ tail -n1 /tmp/demo-tmp-dir-71ab5eeb4a/parallelly-logs/onlylastline.stdout
e
(no newline at end of output)

1 command finished in 0.2 seconds.
+ echo

$ parallelly \
    --cc-args -n3 -a last3lines 'printf "a\nb\nc\nd\ne"'
parallelly will run 1 commands in parallel 
============= Successful command(s) =============
Command last3lines succeeded in 0.0 seconds.
+ printf "a\nb\nc\nd\ne"
/tmp/demo-tmp-dir-71ab5eeb4a/parallelly-logs/last3lines.stderr
/tmp/demo-tmp-dir-71ab5eeb4a/parallelly-logs/last3lines.stdout
STDERR output for successful command last3lines: (no output)
STDOUT output for successful command last3lines: 9 bytes 4 lines
+ tail -n3 /tmp/demo-tmp-dir-71ab5eeb4a/parallelly-logs/last3lines.stdout
c
d
e
(no newline at end of output)

1 command finished in 0.2 seconds.
+ echo

$ parallelly \
    --cc cat -a last3lines 'printf "a\nb\nc\nd\ne"'
parallelly will run 1 commands in parallel 
============= Successful command(s) =============
Command last3lines succeeded in 0.0 seconds.
+ printf "a\nb\nc\nd\ne"
/tmp/demo-tmp-dir-71ab5eeb4a/parallelly-logs/last3lines.stderr
/tmp/demo-tmp-dir-71ab5eeb4a/parallelly-logs/last3lines.stdout
STDERR output for successful command last3lines: (no output)
STDOUT output for successful command last3lines: 9 bytes 4 lines
+ cat  /tmp/demo-tmp-dir-71ab5eeb4a/parallelly-logs/last3lines.stdout
a
b
c
d
e
(no newline at end of output)

1 command finished in 0.1 seconds.

```

### Demo 6: no emoji and no colors


Parallelly prints emoji and colors when it seems they could be supported.
To turn them off, use `--no-color` and `--no-emoji`.

```
$ parallelly \
    --no-color --no-emoji -a long-running 'echo OK >&2 && sleep 0.25' \
    lots-of-output 'cat $(which parallelly)' \
    failing 'echo ERROR ; exit 1'
parallelly will run 3 commands in parallel 
============= Successful command(s) =============
Command long-running succeeded in 0.2 seconds.
+ echo OK >&2 && sleep 0.25
/tmp/demo-tmp-dir-865db193fd/parallelly-logs/long-running.stderr
/tmp/demo-tmp-dir-865db193fd/parallelly-logs/long-running.stdout
STDERR output for successful command long-running: 3 bytes 1 line
+ tail -n1 /tmp/demo-tmp-dir-865db193fd/parallelly-logs/long-running.stderr
OK
STDOUT output for successful command long-running: (no output)

Command lots-of-output succeeded in 0.0 seconds.
+ cat $(which parallelly)
/tmp/demo-tmp-dir-865db193fd/parallelly-logs/lots-of-output.stderr
/tmp/demo-tmp-dir-865db193fd/parallelly-logs/lots-of-output.stdout
STDERR output for successful command lots-of-output: (no output)
STDOUT output for successful command lots-of-output: 36.84 KiBs 1162 lines
+ tail -n1 /tmp/demo-tmp-dir-865db193fd/parallelly-logs/lots-of-output.stdout
# End of parallelly script

============= Failed command output =============
ERROR Failure in command failing after 0.0 seconds.
+ echo ERROR ; exit 1
/tmp/demo-tmp-dir-865db193fd/parallelly-logs/failing.stderr
/tmp/demo-tmp-dir-865db193fd/parallelly-logs/failing.stdout
STDERR output for failed command failing: (no output)
STDOUT output for failed command failing: 6 bytes 1 line
+ tail -n1 /tmp/demo-tmp-dir-865db193fd/parallelly-logs/failing.stdout
ERROR
3 commands finished in 0.8 seconds.
ERROR 1 command failed: failing 

```

### Demo 7: sequential mode


Parallelly supports `--sequential or -s` to run commands sequentially instead of in parallel.
This is useful for testing and comparison purposes.
Also, you can use this mode to just capture output and notify on completion.

```
$ parallelly \
    --sequential -a long-running 'echo OK >&2 && sleep 0.25' \
    lots-of-output 'cat $(which parallelly)' \
    failing 'echo ERROR ; exit 1'
parallelly will run 3 commands sequentially 
FORCE_SEQUENTIAL is set: Waiting for command long-running to finish
FORCE_SEQUENTIAL is set: Waiting for command lots-of-output to finish
FORCE_SEQUENTIAL is set: Waiting for command failing to finish
============= Successful command(s) =============
Command long-running succeeded in 0.2 seconds.
+ echo OK >&2 && sleep 0.25
/tmp/demo-tmp-dir-9c3727b652/parallelly-logs/long-running.stderr
/tmp/demo-tmp-dir-9c3727b652/parallelly-logs/long-running.stdout
STDERR output for successful command long-running: 3 bytes 1 line
+ tail -n1 /tmp/demo-tmp-dir-9c3727b652/parallelly-logs/long-running.stderr
OK
STDOUT output for successful command long-running: (no output)

Command lots-of-output succeeded in 0.0 seconds.
+ cat $(which parallelly)
/tmp/demo-tmp-dir-9c3727b652/parallelly-logs/lots-of-output.stderr
/tmp/demo-tmp-dir-9c3727b652/parallelly-logs/lots-of-output.stdout
STDERR output for successful command lots-of-output: (no output)
STDOUT output for successful command lots-of-output: 36.84 KiBs 1162 lines
+ tail -n1 /tmp/demo-tmp-dir-9c3727b652/parallelly-logs/lots-of-output.stdout
# End of parallelly script

Command failing succeeded in 0.0 seconds.
+ echo ERROR ; exit 1
/tmp/demo-tmp-dir-9c3727b652/parallelly-logs/failing.stderr
/tmp/demo-tmp-dir-9c3727b652/parallelly-logs/failing.stdout
STDERR output for successful command failing: (no output)
STDOUT output for successful command failing: 6 bytes 1 line
+ tail -n1 /tmp/demo-tmp-dir-9c3727b652/parallelly-logs/failing.stdout
ERROR

3 commands finished in 0.9 seconds.

```

### Demo 8: misc arguments


You can show the configuration, the version, or debug information easily.
You can also disable emoji, set the shell used, e.g. to bash, zsh, or fish,
change the arguments passed to tail, and other options.
Use --help to see all options.

```
$ parallelly --trace  # Very noisy!
$ parallelly \
    --show-configuration
============= Configuration =============
Environment variables may have been overridden by command line options.

PARALLELLY_VERBOSE_OUTPUT=false
PARALLELLY_SHOW_ALL_OUTPUT=false
PARALLELLY_EMOJI_OUTPUT=false
CMD_SHELL=sh
CMD_SHELL_ARGS=-c
FORCE_SEQUENTIAL=false
SHOW_CMD_OUTPUT_CMD=tail
SHOW_CMD_OUTPUT_CMD_ARGS=-n1
PARALLELLY_TMP_DIR=/tmp/demo-tmp-dir-8836bf85cb
SHOW_LINE_COUNT=true
SHOW_BYTE_COUNT=true
HUMAN_READABLE_BYTE_COUNT=true
NOTIFY_COMMAND=true
FAILURE_NOTIFY_COMMAND=true
NOTIFY_COMMAND_ARGS=
FAILURE_NOTIFY_COMMAND_ARGS=
ENABLE_COLORS=false
LIGHT_MODE=false
SHOW_CONFIGURATION=true
SHOW_PIDS=false
Temporary directory CMD_OUT_DIR=(unset!)

$ parallelly \
    --no-emoji --light-mode --shell-command bash --cc tail --cc-args -n10 --show-configuration
============= Configuration =============
Environment variables may have been overridden by command line options.

PARALLELLY_VERBOSE_OUTPUT=false
PARALLELLY_SHOW_ALL_OUTPUT=false
PARALLELLY_EMOJI_OUTPUT=false
CMD_SHELL=bash
CMD_SHELL_ARGS=-c
FORCE_SEQUENTIAL=false
SHOW_CMD_OUTPUT_CMD=tail
SHOW_CMD_OUTPUT_CMD_ARGS=-n10
PARALLELLY_TMP_DIR=/tmp/demo-tmp-dir-8836bf85cb
SHOW_LINE_COUNT=true
SHOW_BYTE_COUNT=true
HUMAN_READABLE_BYTE_COUNT=true
NOTIFY_COMMAND=true
FAILURE_NOTIFY_COMMAND=true
NOTIFY_COMMAND_ARGS=
FAILURE_NOTIFY_COMMAND_ARGS=
ENABLE_COLORS=false
LIGHT_MODE=true
SHOW_CONFIGURATION=true
SHOW_PIDS=false
Temporary directory CMD_OUT_DIR=(unset!)

$ parallelly \
    --version
1.11.2
$ parallelly \
    --debug
DEBUG: arglog: Remaining (0)
DEBUG: PPID=<omitted>
DEBUG: Parent process name: bash
DEBUG: Is a TTY: false
DEBUG: Colors supported: 0

```
