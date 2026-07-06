# TODO CLI

A small, well-tested command-line TODO manager built with [Typer](https://typer.tiangolo.com/)
and [Rich](https://rich.readthedocs.io/).

## Features

- Add, list, complete, remove, and clear tasks
- Priorities (`low` / `medium` / `high`)
- Rich table output
- Atomic JSON storage (crash-safe writes, no half-written files)
- Fully typed, tested with pytest, linted with Ruff + Black + mypy
- CI on GitHub Actions across Python 3.10–3.13

## Installation

```bash
pip install -e ".[dev]"
```

## Usage

```bash
todo add "Buy milk"
todo add "Ship the release" --priority high
todo list
todo list --all        # include completed tasks
todo done 1
todo remove 2
todo clear --yes
```

By default, tasks are stored at `~/.config/todo-cli/todos.json`. Set the
`TODO_CLI_HOME` environment variable to override the storage directory.

## Development

```bash
pip install -e ".[dev]"
pre-commit install

ruff check .
black --check .
mypy src
pytest
```