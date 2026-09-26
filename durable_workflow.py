import sqlite3
from pathlib import Path


class DurableWorkflowStore:
    def __init__(self, path="workflows.db"):
        self.path = str(Path(path))
        with sqlite3.connect(self.path) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS workflows "
                "(id TEXT PRIMARY KEY,state TEXT NOT NULL,payload TEXT NOT NULL)"
            )

    def save(self, workflow_id, state, payload):
        with sqlite3.connect(self.path) as db:
            db.execute(
                "INSERT INTO workflows VALUES(?,?,?) "
                "ON CONFLICT(id) DO UPDATE SET state=excluded.state,payload=excluded.payload",
                (workflow_id, state, payload),
            )

    def load(self, workflow_id):
        with sqlite3.connect(self.path) as db:
            return db.execute(
                "SELECT id,state,payload FROM workflows WHERE id=?", (workflow_id,)
            ).fetchone()
