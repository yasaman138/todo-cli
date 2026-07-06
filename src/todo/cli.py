from __future__ import annotations
import typer
from todo.models import Priority, Task
from todo.exceptions import StorageError, TaskNotFoundError
from todo.storage import TodoStorage
from rich.console import Console
from rich.table import Table

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
def list_tasks(
    show_all: bool = typer.Option(
        False, "--all", "-a", help="Include completed tasks in the listing."
    )
) -> None:
    """list tasks"""
    tasks = _load()
    if not show_all:
        tasks = [task for task in tasks if not task.done]

    if not tasks:
        console.print("[yellow]No tasks to show.[/yellow]")
        return

    table = Table(title="TODO List")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Priority")
    table.add_column("Description")

    for task in tasks:
        status = "[green]\u2714[/green]" if task.done else "[grey58]\u25cb[/grey58]"
        table.add_row(str(task.id), status, task.priority.value, task.description)

    console.print(table)


@app.command()
def done(task_id: int = typer.Argument(..., help="ID of the task to mark complete.")) -> None:
    """mark a task as done"""
    tasks = _load()
    task = _find_or_exit(tasks, task_id)
    task.mark_done()
    _save(tasks)
    console.print(f"[green]Completed[/green] task #{task.id}: {task.description}")


@app.command()
def remove(task_id: int = typer.Argument(..., help="ID of the task to remove.")) -> None:
    """remove a task"""
    tasks = _load()
    task = _find_or_exit(tasks, task_id)
    tasks.remove(task)
    _save(tasks)
    console.print(f"[green]Removed[/green] task #{task.id}: {task.description}")


@app.command()
def clear(
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip the confirmation prompt.")
) -> None:
    """remove all tasks"""
    if not yes and not typer.confirm("This will delete all tasks. Continue?"):
        raise typer.Abort()
    _save([])
    console.print("[green]All tasks cleared.[/green]")


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


def _find_or_exit(tasks: list[Task], task_id: int) -> Task:
    try:
        return TodoStorage.find(tasks, task_id)
    except TaskNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    app()
