from pathlib import Path

import pytest
from typer.testing import CliRunner

from todo.storage import TodoStorage


@pytest.fixture()
def tmp_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TodoStorage:
    test_storage = TodoStorage(path=tmp_path / "todos.json")
    monkeypatch.setattr("todo.cli.storage", test_storage)
    return test_storage


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()
