from __future__ import annotations


class TodoError(Exception):
    """base class for all expected errors in todo_cli"""


class TaskNotFoundError(TodoError):
    """raised when a task id does not exist in storage"""

    def __init__(self, task_id: int) -> None:
        super().__init__(f"Task with id {task_id} was not found.")
        self.task_id = task_id


class StorageError(TodoError):
    """raised when storage can't be read or written."""
