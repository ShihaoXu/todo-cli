"""Command Line Interface (CLI) for taskorg project."""
from datetime import date
import os
from io import StringIO
import pathlib
import rich
from rich.table import Table
from contextlib import contextmanager
from typing import List

import taskorg
from .task import *

import typer
from typing_extensions import Annotated

app = typer.Typer(add_completion=False)


@app.command()
def version():
    """Return version of taskorg application"""
    print(taskorg.__version__)


@app.command()
def add(
    owner: Annotated[str, typer.Argument(help="Owner of the task")],
    summary: Annotated[str, typer.Argument(help="Task description")],
    due_date: Annotated[str, typer.Option("-d", "--due-date", help="Due Date", default_factory=(lambda: date.today().strftime("%Y-%m-%d")))],
    tags: Annotated[str, typer.Option("-t", "--tags", default_factory=list, case_sensitive=False, help="Tags for the task, separated by commas")],
    priority: Annotated[str, typer.Option("-p", "--priority", help="Pick one from three priorities: low, medium, high", case_sensitive=False)] = "low",
):
    """Add a new task to the database."""
    with tasks_db() as db:
        tag_list = [tag.strip() for tag in tags.split(",")]
        db.add_task(Task.from_dict( {
            "owner": owner,
            "summary": summary,
            "due_date": due_date,
            "tags": tag_list,
            "priority": priority,
            "status": "todo"
        }))


@app.command()
def delete(task_id: int):
    """Remove task in db with given id."""
    with tasks_db() as db:
        try:
            db.delete_task(task_id)
        except InvalidTaskId:
            print(f"Error: Invalid task id {task_id}")


def task_sort(t: dict, target: str) -> int:
    if target not in Task.SORT_PROPERTIES:
        raise ValueError(f"Invalid sort target: {target}. Must be one of {Task.SORT_PROPERTIES}")
    try:
        match target:
            case "status":
                return status_rank(t["status"])
            case "priority":
                return priority_rank(t["priority"])
            case _:
                return t[target]
    except KeyError as exc:
        raise TaskException(f"Task: {t} does not have the property '{target}' to sort by.") from exc

    return sorted(tasks, key=lambda t: t[target], reverse=(order == "descending"))


    # def list_tasks(self,
    #                owners=None,
    #                summary=None,
    #                statuses=None,
    #                priorities=None,
    #                due_date=None,
    #                tags=None) -> List[dict]:
# propertys = ["owner", "summary", "status", "priority", "due_date", "tags"]
@app.command("list")
def list_cards(
    sort: Annotated[str, typer.Option(..., "--sort", help="Pick one column for sorting: owner, status, priority, due_date")] = "due_date",
    order: Annotated[str, typer.Option(..., "--order", help="ascending or descending")] = "ascending",
    statuses: Annotated[str | None, typer.Option(..., "--status", help="Filter by status, e.g. todo, in_progress, done")] = None,
    owners: Annotated[str | None, typer.Option(..., "-o", "--owner")] = None,
    summary: Annotated[str | None, typer.Option(..., "-s", "--summary")] = None,
    due_date: Annotated[str | None, typer.Option(..., "-d", "--due-date")] = None,
    tags: Annotated[str | None, typer.Option(..., "-t", "--tags")] = None,
    priorities: Annotated[str | None, typer.Option(..., "-p", "--priority")] = None,
):
    """Filter and list tasks in db."""
    with tasks_db() as db:
        the_tasks = db.list_tasks(owners, summary, statuses, priorities, due_date, tags)
        sorted_tasks = sorted(the_tasks, key=lambda t: task_sort(t, sort), reverse=(order == "descending"))

        table = Table()
        table.add_column("ID")
        table.add_column("Owner")
        table.add_column("Summary")
        table.add_column("Status")
        table.add_column("Priority")
        table.add_column("Due Date")
        table.add_column("Tags")
        
        for t in sorted_tasks:
            table.add_row(str(t["id"]), t["owner"], t["summary"], t["status"], t["priority"], t["due_date"], ", ".join(t["tags"]) if t["tags"] else "")
        out = StringIO()
        rich.print(table, file=out)
        print(out.getvalue())

@app.command()
def update(
    task_id: int,
    owner: Annotated[str | None, typer.Option(..., "-o", "--owner")] = None,
    summary: Annotated[str | None, typer.Option(..., "-s", "--summary")] = None,
    due_date: Annotated[str | None, typer.Option(..., "-d", "--due-date")] = None,
    tags: Annotated[str | None, typer.Option(..., "-t", "--tags")] = None,
    priority: Annotated[str | None, typer.Option(..., "-p", "--priority")] = None,
):
    """Modify a task in db with given id with new info."""
    with tasks_db() as db:
        task_mods = {
            "owner": owner,
            "summary": summary,
            "due_date": due_date,
            "tags": [tag.strip() for tag in tags.split(",")] if tags else None,
            "priority": priority
        }

        try:
            db.update_task(task_id, Task.from_dict({k: task_mods[k] for k in Task.UPDATE_PROPERTIES if k is not None}))
        except InvalidTaskId:
            print(f"Error: Invalid task id {task_id}")


@app.command()
def start(task_id: int):
    """Set a task state to 'in prog'."""
    with tasks_db() as db:
        try:
            db.start(task_id)
        except InvalidTaskId:
            print(f"Error: Invalid task id {task_id}")


@app.command()
def finish(task_id: int):
    """Set a card state to 'done'."""
    with tasks_db() as db:
        try:
            db.finish(task_id)
        except InvalidTaskId:
            print(f"Error: Invalid card id {task_id}")


@app.command()
def config():
    """List the path to the Cards db."""
    with tasks_db() as db:
        print(db.path())


@app.command()
def count():
    """Return number of cards in db."""
    with tasks_db() as db:
        print(db.count())


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Taskorg is a small command line task tracking application.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(list_cards)


def get_path():
    db_path_env = os.getenv("TASKS_DB_DIR", "")
    if db_path_env:
        db_path = pathlib.Path(db_path_env)
    else:
        db_path = pathlib.Path.home() / "tasks_db"
    return db_path


@contextmanager
def tasks_db():
    db_path = get_path()
    db = taskorg.TaskDB(db_path)
    yield db
    db.close()
