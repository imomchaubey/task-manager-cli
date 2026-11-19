"""Command‑line interface for the task manager.

The CLI is intentionally thin – it parses arguments, forwards them to
:class:`~task_manager.TaskManager`, and prints human‑readable output.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

from task_manager import TaskManager, Task


def _print_tasks(tasks: List[Task]) -> None:
    """Print a list of tasks to stdout.

    Each line contains the task id, a completion marker and the description.
    Example:
        [ ] 1: Buy milk
        [x] 2: Write docs
    """
    for task in tasks:
        marker = "x" if task.completed else " "
        print(f"[{marker}] {task.id}: {task.description}")


def build_parser() -> argparse.ArgumentParser:
    """Create the top‑level argument parser."""
    parser = argparse.ArgumentParser(
        prog="taskmgr",
        description="Simple JSON‑backed task manager.",
    )
    parser.add_argument(
        "--store",
        type=Path,
        default=Path("tasks.json"),
        help="Path to the JSON store (default: tasks.json in cwd).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # add --------------------------------------------------------------
    add_parser = subparsers.add_parser("add", help="Add a new task.")
    add_parser.add_argument("description", help="Description of the new task.")

    # list -------------------------------------------------------------
    subparsers.add_parser("list", help="List all tasks.")

    # complete ---------------------------------------------------------
    complete_parser = subparsers.add_parser(
        "complete", help="Mark a task as completed."
    )
    complete_parser.add_argument("id", type=int, help="ID of the task to complete.")

    # delete -----------------------------------------------------------
    delete_parser = subparsers.add_parser("delete", help="Delete a task.")
    delete_parser.add_argument("id", type=int, help="ID of the task to delete.")

    return parser


def main(argv: List[str] | None = None) -> None:
    """Entry point for the console script.

    Parameters
    ----------
    argv:
        Optional list of arguments (excluding the program name).  If ``None``,
        ``sys.argv[1:]`` is used.  This signature makes the function easy to
        test.
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    manager = TaskManager(args.store)

    if args.command == "add":
        task = manager.add(args.description)
        print(f"Added task {task.id}: {task.description}")

    elif args.command == "list":
        tasks = manager.list_all()
        if not tasks:
            print("No tasks.")
        else:
            _print_tasks(tasks)

    elif args.command == "complete":
        try:
            manager.complete(args.id)
            print(f"Task {args.id} marked as completed.")
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            sys.exit(1)

    elif args.command == "delete":
        try:
            manager.delete(args.id)
            print(f"Task {args.id} deleted.")
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
