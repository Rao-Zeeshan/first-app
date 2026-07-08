"""
Simple Todo List CLI Application
Usage:
    python app.py add "Buy groceries"
    python app.py list
    python app.py done 1
    python app.py delete 1
"""

import json
import os
import sys
import argparse
from rich.console import Console
from rich.table import Table

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")
console = Console()


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(title):
    tasks = load_tasks()
    tasks.append({"id": len(tasks) + 1, "title": title, "done": False})
    save_tasks(tasks)
    console.print(f"[green]Added:[/green] {title}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        console.print("[yellow]No tasks found. Add one with 'add'.[/yellow]")
        return

    table = Table(title="Todo List")
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Task", style="white")
    table.add_column("Status", style="magenta", justify="center")

    for t in tasks:
        status = "[green]Done[/green]" if t["done"] else "[red]Pending[/red]"
        table.add_row(str(t["id"]), t["title"], status)

    console.print(table)


def mark_done(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            console.print(f"[green]Marked task {task_id} as done.[/green]")
            return
    console.print(f"[red]Task {task_id} not found.[/red]")


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        console.print(f"[red]Task {task_id} not found.[/red]")
        return
    # re-number ids
    for i, t in enumerate(new_tasks, start=1):
        t["id"] = i
    save_tasks(new_tasks)
    console.print(f"[green]Deleted task {task_id}.[/green]")


def main():
    parser = argparse.ArgumentParser(description="Simple Todo List CLI App")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("title", type=str, help="Task description")

    subparsers.add_parser("list", help="List all tasks")

    done_p = subparsers.add_parser("done", help="Mark a task as done")
    done_p.add_argument("id", type=int, help="Task ID")

    delete_p = subparsers.add_parser("delete", help="Delete a task")
    delete_p.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        mark_done(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
