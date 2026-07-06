from __future__ import annotations
import typer
from todo.models import Priority, Task
from todo.storage import StorageError, TodoStorage
from rich.console import Console

app = typer.Typer(add_completion=False, help="A simple, fast command-line TODO manager.")
console = Console()
storage = TodoStorage()


@app.command()
def add(
    description: str = typer.Argument(..., help="What needs to be done."),
    priority: Priority = typer.Option(
        Priority.MEDIUM, "--priority", "-p", case_sensitive=False, help="Task priority."
    ),
) -> None:
    """add a new task"""
    tasks = _load()
    task = Task(id=TodoStorage.next_id(tasks), description=description, priority=priority)
    tasks.append(task)
    _save(tasks)
    console.print(f"[green]Added[/green] task #{task.id}: {task.description}")


@app.command(name="list")
def list_tasks() -> None:
    """list tasks"""


@app.command()
def done() -> None:
    """mark a task as done"""


@app.command()
def remove() -> None:
    """remove a task"""


@app.command()
def clear() -> None:
    """remove all tasks"""


def _load() -> list[Task]:
    try:
        return storage.load()
    except StorageError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc


def _save(tasks: list[Task]) -> None:
    try:
        storage.save(tasks)
    except StorageError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    app()
