import json
import os
from pathlib import Path

# Get the directory where this script is located
BASE_DIR = Path(__file__).parent.parent.parent

# Build the path to your data file, relative to this script
DATA_FILE = BASE_DIR / "data" / "tasks.json"


def save_tasks(task_master, next_id, filename=DATA_FILE):
    # Save the task list and next_id to a JSON file.
    data = {"tasks": task_master, "next_id": next_id}
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_tasks(filename=DATA_FILE):
    # Load the task list and next_id from a JSON file.
    if not os.path.exists(filename):
        return [], 1  # Empty list, start next_id at 1
    with open(filename, "r") as f:
        data = json.load(f)
        return data.get("tasks", []), data.get("next_id", 1)
