from datetime import date
from storage import save_tasks, DATA_FILE
from tabulate import tabulate


def add_task(task_master, description, next_id, filename=DATA_FILE):
    # Add a new task to the task master list with an incremental ID.
    today = date.today()
    creation_date = today.strftime("%d-%m-%Y")
    task = {
        "id": next_id,
        "description": description,
        "status": False,
        "creation_date": creation_date,
    }
    task_master.append(task)
    save_tasks(task_master, next_id + 1, filename)

    return task, next_id + 1


def list_tasks(task_master):
    # Display all tasks in a formatted table using tabulate.
    if not task_master:
        print("No tasks found.")
        return

    # Prepare data for tabulate
    table_data = []
    for task in task_master:
        status = "Done" if task["status"] else "Pending"
        table_data.append(
            [task["id"], status, task["description"], task["creation_date"]]
        )

    headers = ["ID", "Status", "Description", "Created On"]
    print(tabulate(table_data, headers=headers, tablefmt="mixed_grid"))


def list_pending_tasks(task_master):
    # Display only tasks that are not yet completed.
    pending_tasks = [task for task in task_master if not task["status"]]

    if not pending_tasks:
        print("No pending tasks!")
        return

    table_data = [
        [task["id"], task["description"], task["creation_date"]]
        for task in pending_tasks
    ]
    headers = ["ID", "Description", "Created On"]
    print(tabulate(table_data, headers=headers, tablefmt="rounded_grid"))


def remove_task(task_master, task_id, next_id, filename=DATA_FILE):
    # Delete a task by ID. Returns True if deleted, False if not found.
    for i, task in enumerate(task_master):
        if task["id"] == task_id:
            del task_master[i]
            save_tasks(task_master, next_id, filename)
            return True
    return False


def remove_all_tasks(task_master):
    # Remove all tasks.
    task_master.clear()
    return True


def remove_completed_tasks(task_master):
    # Remove all completed (done) tasks.
    original_count = len(task_master)
    task_master[:] = [task for task in task_master if not task["status"]]
    return len(task_master) < original_count  # Returns True if any were removed


def mark_task_done(task_master, task_id, next_id, filename=DATA_FILE):
    # Mark a task as done by ID. Returns True if updated, False if not found.
    for task in task_master:
        if task["id"] == task_id:
            task["status"] = True
            save_tasks(task_master, next_id, filename)
            return True
    return False
