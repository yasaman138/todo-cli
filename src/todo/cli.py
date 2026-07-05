import typer

app = typer.Typer(add_completion=False, help="A simple, fast command-line TODO manager.")


@app.command
def add() -> None:
    """add a new task"""


@app.command
def list_tasks() -> None:
    """list tasks"""


@app.command
def done() -> None:
    """mark a task as done"""


@app.command
def remove() -> None:
    """remove a task"""


@app.command
def clear() -> None:
    """remove all tasks"""


if __name__ == "__main__":
    app()
