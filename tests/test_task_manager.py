import json
from pathlib import Path

import pytest

from task_manager import TaskManager


@pytest.fixture
def empty_store(tmp_path):
    """Provide a fresh TaskManager backed by an isolated JSON file."""
    store = tmp_path / "tasks.json"
    store.write_text("[]")
    return TaskManager(store)


def test_add_and_list(empty_store):
    # happy path: add two tasks and verify list output
    empty_store.add("Buy milk")
    empty_store.add("Write docs")
    tasks = empty_store.list_all()
    assert len(tasks) == 2
    assert tasks[0].description == "Buy milk"
    assert tasks[1].description == "Write docs"

    # also verify file persistence
    data = json.loads(Path(empty_store.file_path).read_text())
    assert data[0]["description"] == "Buy milk"


def test_complete(empty_store):
    empty_store.add("Finish report")
    task = empty_store.list_all()[0]
    empty_store.complete(task.id)
    updated = empty_store.list_all()[0]
    assert updated.completed is True

    # ensure JSON reflects change
    data = json.loads(Path(empty_store.file_path).read_text())
    assert data[0]["completed"] is True


def test_delete_and_error_handling(empty_store):
    empty_store.add("Task to remove")
    task = empty_store.list_all()[0]

    # delete existing task
    empty_store.delete(task.id)
    assert empty_store.list_all() == []

    # trying to delete a non‑existent id should raise ValueError
    with pytest.raises(ValueError):
        empty_store.delete(999)


def test_cli_add_list(tmp_path, capsys):
    # integration‑style test using the CLI entry point
    from cli import main

    store = tmp_path / "tasks.json"
    store.write_text("[]")

    # simulate command line args
    main(["--store", str(store), "add", "CLI task"])
    main(["--store", str(store), "list"])

    captured = capsys.readouterr()
    assert "CLI task" in captured.out
