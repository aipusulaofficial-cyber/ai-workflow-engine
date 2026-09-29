import sqlite3
from pathlib import Path

from workflow_domain import State


class DurableWorkflowStore:
    """Transactional workflow store with guarded lifecycle changes."""

    _ALLOWED = {
        State.PENDING: {State.RUNNING, State.FAILED},
        State.RUNNING: {State.SUCCEEDED, State.FAILED},
        State.SUCCEEDED: set(),
        State.FAILED: set(),
    }

    def __init__(self, path="workflows.db"):
        self.path = str(Path(path))
        with sqlite3.connect(self.path) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS workflows "
                "(id TEXT PRIMARY KEY,state TEXT NOT NULL,payload TEXT NOT NULL)"
            )

    def save(self, workflow_id, state, payload):
        if not workflow_id:
            raise ValueError("workflow id is required")
        target = State(state)
        with sqlite3.connect(self.path, isolation_level="IMMEDIATE") as db:
            row = db.execute("SELECT state FROM workflows WHERE id=?", (workflow_id,)).fetchone()
            if row is None:
                if target != State.PENDING:
                    raise ValueError("new workflow must start pending")
                db.execute(
                    "INSERT INTO workflows VALUES(?,?,?)",
                    (workflow_id, target.value, payload),
                )
            else:
                current = State(row[0])
                if target != current and target not in self._ALLOWED[current]:
                    raise ValueError(f"invalid workflow transition {current}->{target}")
                db.execute(
                    "UPDATE workflows SET state=?,payload=? WHERE id=?",
                    (target.value, payload, workflow_id),
                )

    def load(self, workflow_id):
        with sqlite3.connect(self.path) as db:
            return db.execute(
                "SELECT id,state,payload FROM workflows WHERE id=?", (workflow_id,)
            ).fetchone()
