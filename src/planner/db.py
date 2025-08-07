"""
DB for the todo-cli project
"""
import tinydb

# Owner, Summary, ID, Status, Priority, DueDate, Tags

class DB:
    def __init__(self, db_path, db_file):
        self._db = tinydb.TinyDB(db_path / f"{db_file}.json", create_dirs=True)

    def create(self, item: dict) -> int:
        return self._db.insert(item)

    def read(self, task_id: int):
        return self._db.get(doc_id=task_id)

    def read_all(self):
        return self._db

    def update(self, task_id: int, mods) -> None:
        changes = {k: v for k, v in mods.items() if v is not None}
        self._db.update(changes, doc_ids=[task_id])

    def delete(self, task_id: int) -> None:
        self._db.remove(doc_ids=[task_id])

    def delete_all(self) -> None:
        self._db.truncate()

    def count(self) -> int:
        return len(self._db)

    def close(self):
        self._db.close()
