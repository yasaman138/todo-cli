from __future__ import annotations
from pathlib import Path
import os
from todo.models import Task
import json
from todo.exceptions import StorageError, TaskNotFoundError
from collections.abc import Iterable
import tempfile


class TodoStorage:
    def __init__(self, path: Path | None = None):
        self.path = path or self._default_path()

    @staticmethod
    def _default_path() -> Path:
        override = os.environ.get("TODO_CLI_HOME")
        base = Path(override) if override else Path.home() / ".config" / "todo_cli"
        return base / "todos.json"

    def load(self) -> list[Task]:
        """load all tasks, or an empty list if no task exists yet."""
        if not self.path.exists():
            return []

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise StorageError(f"Corrupted todo file at {self.path}: {exc}") from exc
        except OSError as exc:
            raise StorageError(f"Could not read todo file at {self.path}: {exc}") from exc

        return [Task.from_dict(item) for item in raw]

    def save(self, tasks: Iterable[Task]) -> None:
        payload = [task.to_dict() for task in tasks]
        self.path.parent.mkdir(parents=True, exist_ok=True)

        fd, tmp_name = tempfile.mkstemp(dir=self.path.parent, prefix=".todos-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, ensure_ascii=False)
            os.replace(tmp_name, self.path)
        except OSError as exc:
            Path(tmp_name).unlink(missing_ok=True)
            raise StorageError(f"Could not write todo file at {self.path}: {exc}") from exc

    @staticmethod
    def next_id(tasks: Iterable[Task]) -> int:
        """compute the next free task id"""
        return max((task.id for task in tasks), default=0) + 1

    @staticmethod
    def find(tasks: list[Task], task_id: int) -> Task:
        """return the task with the given id, or raise TaskNotFoundError"""
        for task in tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(task_id)
