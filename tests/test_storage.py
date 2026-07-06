from pathlib import Path

import pytest

from todo.exceptions import StorageError, TaskNotFoundError
from todo.models import Task
from todo.storage import TodoStorage


def test_load_returns_empty_list_when_file_missing(tmp_path: Path) -> None:
    storage = TodoStorage(path=tmp_path / "missing.json")
    assert storage.load() == []


def test_save_and_load_round_trip(tmp_path: Path) -> None:
    storage = TodoStorage(path=tmp_path / "todos.json")
    storage.save([Task(id=1, description="Buy milk")])

    loaded = storage.load()
    assert len(loaded) == 1
    assert loaded[0].description == "Buy milk"


def test_load_raises_error_on_corrupted_file(tmp_path: Path) -> None:
    path = tmp_path / "todos.json"
    path.write_text("{not valid json", encoding="utf-8")
    storage = TodoStorage(path=path)
    with pytest.raises(StorageError):
        storage.load()


def test_next_id_increments_from_max() -> None:
    tasks = [Task(id=1, description="a"), Task(id=5, description="b")]
    assert TodoStorage.next_id(tasks) == 6


def test_next_id_starts_at_one_when_empty() -> None:
    assert TodoStorage.next_id([]) == 1


def test_find_returns_matching_task() -> None:
    tasks = [Task(id=1, description="a"), Task(id=2, description="b")]
    assert TodoStorage.find(tasks, 2).description == "b"


def test_find_raises_task_not_found() -> None:
    with pytest.raises(TaskNotFoundError):
        TodoStorage.find([], 99)
