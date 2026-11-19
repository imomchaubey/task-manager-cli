# Simple Task Manager

A tiny command‑line utility that lets you keep a list of tasks in a
single JSON file (`tasks.json` by default).  It supports four basic
operations:

| Command | Description |
|---------|-------------|
| `add "description"` | Create a new task |
| `list` | Show all tasks |
| `complete &lt;id&gt;` | Mark a task as done |
| `delete &lt;id&gt;` | Remove a task |

The heavy lifting is done by **`task_manager.py`**, a pure‑Python
library that can be imported and used programmatically.  The CLI is a
thin wrapper around this library.

## Installation

```bash
git clone <repo‑url>
cd <repo>
pip install -r requirements.txt
```

## Usage

```bash
# add a task
python cli.py add "Buy milk"

# show all tasks
python cli.py list

# mark task 1 as completed
python cli.py complete 1

# delete task 2
python cli.py delete 2
```

You can also point the manager at a custom JSON file:

```bash
python cli.py --store /tmp/mytasks.json add "Custom location"
```

## Testing

The test suite lives in the `tests/` directory and uses **pytest**.

```bash
pytest -q
```

All tests should pass, confirming that the library correctly handles
adding, listing, completing, and deleting tasks, and that the CLI
produces the expected output.

## License

MIT – feel free to copy, modify, and redistribute.
