from typer.testing import CliRunner

from todo.cli import app


def test_add_and_list(runner: CliRunner) -> None:
    result = runner.invoke(app, ["add", "Test task"])
    assert result.exit_code == 0
    assert "Added" in result.stdout

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Test task" in result.stdout


def test_add_with_priority(runner: CliRunner) -> None:
    result = runner.invoke(app, ["add", "Urgent thing", "--priority", "high"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["list"])
    assert "high" in result.stdout


def test_list_empty(runner: CliRunner) -> None:
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "No tasks" in result.stdout


def test_done_marks_task_complete_and_hides_it_by_default(runner: CliRunner) -> None:
    runner.invoke(app, ["add", "Task A"])

    result = runner.invoke(app, ["done", "1"])
    assert result.exit_code == 0
    assert "Completed" in result.stdout

    result = runner.invoke(app, ["list"])
    assert "Task A" not in result.stdout

    result = runner.invoke(app, ["list", "--all"])
    assert "Task A" in result.stdout


def test_done_unknown_task_exits_nonzero(runner: CliRunner) -> None:
    result = runner.invoke(app, ["done", "42"])
    assert result.exit_code == 1


def test_remove_task(runner: CliRunner) -> None:
    runner.invoke(app, ["add", "Task B"])

    result = runner.invoke(app, ["remove", "1"])
    assert result.exit_code == 0
    assert "Removed" in result.stdout

    result = runner.invoke(app, ["list"])
    assert "Task B" not in result.stdout


def test_remove_unknown_task_exits_nonzero(runner: CliRunner) -> None:
    result = runner.invoke(app, ["remove", "42"])
    assert result.exit_code == 1


def test_clear_with_flag_skips_prompt(runner: CliRunner) -> None:
    runner.invoke(app, ["add", "Task C"])

    result = runner.invoke(app, ["clear", "--yes"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["list", "--all"])
    assert "No tasks" in result.stdout


def test_clear_without_flag_prompts_for_confirmation(runner: CliRunner) -> None:
    runner.invoke(app, ["add", "Task D"])

    result = runner.invoke(app, ["clear"], input="n\n")
    assert result.exit_code != 0

    result = runner.invoke(app, ["list", "--all"])
    assert "Task D" in result.stdout
