# RTUI - Robot Terminal User Interface

A TUI for [Astoria](https://github.com/srobo/astoria)-driven robots.

[![asciicast](https://asciinema.org/a/NJoUTaZ0G7VcotlNVgL7iXufR.svg)](https://asciinema.org/a/NJoUTaZ0G7VcotlNVgL7iXufR)

## Usage

The `rtui` command can be used standalone by running `rtui`.

It can also be used as an SSH forced command by adding the following to the `authorized_keys` file:

```
command="/usr/bin/rtui" ssh-ed25519 AAAA....
```

### Available Commands

- `arena`: Get or set the current arena
- `exit`: Leave the terminal session.
- `help`: Show available commands
- `kill`: Kill running code
- `metadata`: Show all robot metadata
- `mode`: Get or set the current robot mode (COMP or DEV)
- `quit`: Leave the terminal session.
- `restart`: Restart running code
- `start`: Trigger the virtual start button
- `trigger`: Trigger the virtual start button
- `zone`: Get or set the current zone


## Development

This application is written in Python 3.8+ and is managed using poetry.

```shell
poetry install
poetry run rtui
```

You will need to have an instance of Astoria running for some functionality, the docker setup is recommended for this.