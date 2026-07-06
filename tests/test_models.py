from datetime import datetime

from todo.models import Priority, Task


def test_task_defaults() -> None:
    task = Task(id=1, description="")
    assert task.done is False
    assert task.priority is Priority.MEDIUM
    assert isinstance(task.created_at, datetime)
    assert task.completed_at is None


def test_mark_done_sets_completed_at() -> None:
    task = Task(id=1, description="for checking completed_at")
    task.mark_done()
    assert task.done is True
    assert task.completed_at is not None


def test_round_trip_serialization() -> None:
    task = Task(id=2, description="for checking json serialization", priority=Priority.HIGH)
    restored = Task.from_dict(task.to_dict())
    assert restored.id == task.id
    assert restored.description == task.description
    assert restored.priority == task.priority
    assert restored.created_at == task.created_at
