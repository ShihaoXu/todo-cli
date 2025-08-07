from datetime import datetime
from typing import List
from .db import DB
from .task import *
import re

class TaskDB:
    def __init__(self, db_path):
        self._db_path = db_path
        self._db = DB(db_path, ".Tasks_db")

    def add_task(self, task: Task) -> int:
        """Add a task, return the id of task."""
        task_id = self._db.create(task.to_dict())
        self._db.update(task_id, {"id": task_id}) # modify the task with its id
        return task_id

    def get_task(self, task_id: int) -> Task:
        """Return a task with a matching id."""
        db_item = self._db.read(task_id)
        if db_item is None:
            raise InvalidTaskId(task_id)

        try:
            task = Task.from_dict(db_item)
        except TaskException as exc:
            raise exc

        return task

    def list_tasks(self,
                   owners=None,
                   summary=None,
                   statuses=None,
                   priorities=None,
                   due_date=None,
                   tags=None) -> List[dict]:
        """Return a list of tasks."""
        selected_tasks = [ dict(t) for t in self._db.read_all() ]
        if owners:
            selected_tasks = [t for t in selected_tasks if t["owner"] in owners]
        if summary:
            selected_tasks = [t for t in selected_tasks if re.search(summary, t["summary"], re.IGNORECASE)]
        if statuses:
            selected_tasks = [t for t in selected_tasks if t["status"] in statuses]
        if priorities:
            selected_tasks = [t for t in selected_tasks if t["priority"] in priorities]
        if due_date:
            selected_tasks = [
                t for t in selected_tasks 
                if datetime.strptime(t["due_date"], "%Y-%m-%d").date() <=
                    datetime.strptime(due_date, "%Y-%m-%d").date()
                ]
        if tags:
            selected_tasks = [t for t in selected_tasks if any(tag in t["tags"] for tag in tags)]
        return selected_tasks

    def count(self) -> int:
        """Return the number of tasks in db."""
        return self._db.count()

    def update_task(self, task_id: int, task_mods: Task) -> None:
        """Update a task with modifications."""
        try:
            self._db.update(task_id, task_mods.to_dict())
        except KeyError as exc:
            raise InvalidTaskId(task_id) from exc

    def start(self, task_id: int):
        """Set a task state to 'in prog'."""
        self.update_task(task_id, Task(status="in_progress"))

    def finish(self, task_id: int):
        """Set a task state to 'done'."""
        self.update_task(task_id, Task(status="done"))

    def delete_task(self, task_id: int) -> None:
        """Remove a task from db with given task_id."""
        try:
            self._db.delete(task_id)
        except KeyError as exc:
            raise InvalidTaskId(task_id) from exc

    def delete_all(self) -> None:
        """Remove all tasks from db."""
        self._db.delete_all()

    def close(self):
        self._db.close()

    def path(self):
        return self._db_path
