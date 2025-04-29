import argparse
from todo.storage import load_tasks, save_tasks
from todo.tasks import (
    add_task,
    list_tasks,
    list_pending_tasks,
    remove_task,
    remove_all_tasks,
    remove_completed_tasks,
    mark_task_done,
)


def main():
    task_master, next_id = load_tasks()

    parser = argparse.ArgumentParser(description="Simple Todo CLI App")
    subparsers = parser.add_subparsers(dest="command")

    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", type=str, help="Task description")

    parser_list = subparsers.add_parser("list", help="List all tasks")
    parser_list.add_argument(
        "-p", "--pending", action="store_true", help="Show only pending tasks"
    )

    parser_remove = subparsers.add_parser("remove", help="Remove a task by ID")
    parser_remove.add_argument(
        "task_id", type=int, nargs="?", help="ID of the task to remove"
    )
    parser_remove.add_argument("--all", action="store_true", help="Remove all tasks")
    parser_remove.add_argument(
        "-d", "--done", action="store_true", help="Remove completed tasks"
    )

    parser_mark = subparsers.add_parser("update", help="Mark a task as done by ID")
    parser_mark.add_argument("task_id", type=int, help="ID of the task to mark")

    args = parser.parse_args()

    if args.command == "add":
        task, next_id = add_task(task_master, args.description, next_id)
        print(f"Added: {task['description']} (ID: {task['id']})")

    elif args.command == "list":
        if args.pending:
            list_pending_tasks(task_master)
        else:
            list_tasks(task_master)

    elif args.command == "remove":
        if args.all:
            remove_all_tasks(task_master)
            print("All tasks removed")
        elif args.done:
            if remove_completed_tasks(task_master):
                print("All completed tasks removed")
            else:
                print("No task to remove")
        elif args.task_id is not None:
            if remove_task(task_master, args.task_id, next_id):
                print(f"Task {args.task_id} deleted.")
            else:
                print(f"Task {args.task_id} not found.")
        else:
            print("Please specify a task ID, --all, or --done.")

    elif args.command == "update":
        if mark_task_done(task_master, args.task_id, next_id):
            print(f"Task {args.task_id} marked as done.")
        else:
            print(f"Task {args.task_id} not found.")

    else:
        parser.print_help()

    save_tasks(task_master, next_id)


if __name__ == "__main__":
    main()
