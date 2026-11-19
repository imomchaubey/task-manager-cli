"""Task manager core library.

Provides a simple JSON‑backed task list with CRUD operations.
All functionality is independent of any command‑line interface,
making it easy to import and test.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass
class Task:
    """A single to‑do item."""

    id: int
    description: str
    completed: bool = False


class TaskManager:
    """Manage a collection of :class:`Task` objects stored in a JSON file."""

    def __init__(self, store_path: Path | str) -> None:
        """
        Parameters
        ----------
        store_path:
            Path to the JSON file used for persistence.  If the file does not
            exist it will be created automatically with an empty list.
        """
        self.file_path = Path(store_path)
        # Ensure the file exists with a valid JSON array.
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")
        self._tasks: List[Task] = self._load()

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    def _load(self) -> List[Task]:
        """Load tasks from ``self.file_path``."""
        try:
            raw = json.loads(self.file_path.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                raise ValueError("Corrupted store: expected a list at top level")
        except json.JSONDecodeError as exc:
            raise ValueError(f"Corrupted JSON store: {exc}") from exc

        tasks = []
        for entry in raw:
            try:
                tasks.append(Task(**entry))
            except TypeError as exc:
                raise ValueError(f"Invalid task entry in store: {entry}") from exc
        return tasks

    def _save(self) -> None:
        """Write the current task list to ``self.file_path``."""
        serialisable = [asdict(task) for task in self._tasks]
        self.file_path.write_text(json.dumps(serialisable, indent=2), encoding="utf-8")

    def _next_id(self) -> int:
        """Return the next free integer ID."""
        if not self._tasks:
            return 1
        return max(task.id for task in self._tasks) + 1

    def _find_index(self, task_id: int) -> int:
        """Return the list index of the task with *task_id* or raise ValueError."""
        for idx, task in enumerate(self._tasks):
            if task.id == task_id:
                return idx
        raise ValueError(f"Task with id {task_id} not found")

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def add(self, description: str) -> Task:
        """Create a new task and persist it.

        Parameters
        ----------
        description:
            Human‑readable description of the task.

        Returns
        -------
        Task
            The newly created task instance.
        """
        if not description:
            raise ValueError("Task description cannot be empty")
        task = Task(id=self._next_id(), description=description, completed=False)
        self._tasks.append(task)
        self._save()
        return task

    def list_all(self) -> List[Task]:
        """Return a shallow copy of all stored tasks."""
        return list(self._tasks)

    def complete(self, task_id: int) -> None:
        """Mark the task identified by *task_id* as completed.

        Raises
        ------
        ValueError
            If the task does not exist.
        """
        idx = self._find_index(task_id)
        self._tasks[idx].completed = True
        self._save()

    def delete(self, task_id: int) -> None:
        """Remove the task identified by *task_id*.

        Raises
        ------
        ValueError
            If the task does not exist.
        """
        idx = self._find_index(task_id)
        del self._tasks[idx]
        self._save()
