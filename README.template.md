# parallelly: Run commands in parallel and capture output. Notify on each completion.

<!--
EDIT README.template.md, not README.md directly.
Use `make build-readme to update the README file
-->

Add synchronized swimming to your CLI!

## Usage

See [demos at bottom of document](#demos) for examples with output.

```
<HELP_STRING>
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

<DEMO_OUTPUT>
