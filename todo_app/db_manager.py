import sqlite3
from datetime import datetime
from pathlib import Path


class DBManager:
    """SQLite database manager for tasks and notes."""

    def __init__(self, db_path: str = "tasks_notes.db"):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.create_tables()

    def create_tables(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                due_date TEXT,
                priority INTEGER,
                status TEXT DEFAULT 'pending'
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS notes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                last_modified TEXT
            )
            """
        )
        self.conn.commit()

    # Task methods
    def add_task(self, title: str, due_date: str | None = None, priority: int = 0) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO tasks(title, due_date, priority, status) VALUES(?,?,?,?)",
            (title, due_date, priority, "pending"),
        )
        self.conn.commit()
        return cur.lastrowid

    def update_task(self, task_id: int, **kwargs) -> None:
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in {"title", "due_date", "priority", "status"}:
                fields.append(f"{key} = ?")
                values.append(value)
        if not fields:
            return
        values.append(task_id)
        self.conn.execute(
            f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", values
        )
        self.conn.commit()

    def delete_task(self, task_id: int) -> None:
        self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def list_tasks(self) -> list[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, title, due_date, priority, status FROM tasks ORDER BY id"
        )
        return cur.fetchall()

    # Note methods
    def add_note(self, title: str, content: str = "") -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO notes(title, content, last_modified) VALUES(?,?,?)",
            (title, content, datetime.utcnow().isoformat()),
        )
        self.conn.commit()
        return cur.lastrowid

    def update_note(self, note_id: int, **kwargs) -> None:
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in {"title", "content"}:
                fields.append(f"{key} = ?")
                values.append(value)
        if not fields:
            return
        fields.append("last_modified = ?")
        values.append(datetime.utcnow().isoformat())
        values.append(note_id)
        self.conn.execute(
            f"UPDATE notes SET {', '.join(fields)} WHERE id = ?", values
        )
        self.conn.commit()

    def delete_note(self, note_id: int) -> None:
        self.conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.conn.commit()

    def list_notes(self) -> list[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, title, content, last_modified FROM notes ORDER BY id")
        return cur.fetchall()

    def close(self) -> None:
        self.conn.close()
