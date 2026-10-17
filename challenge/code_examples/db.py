"""
db.py — Learnify database helper utilities
Reference implementation used across platform services.
"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

DB_PATH = Path(__file__).parent.parent / "data" / "platform.db"


@contextmanager
def get_conn() -> Generator[sqlite3.Connection, None, None]:
    """Context manager that always commits or rolls back cleanly."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetch_one(query: str, params: tuple = ()) -> dict | None:
    """Return the first matching row as a dict, or None."""
    with get_conn() as conn:
        row = conn.execute(query, params).fetchone()
        return dict(row) if row else None


def fetch_all(query: str, params: tuple = ()) -> list[dict]:
    """Return all matching rows as a list of dicts."""
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(query, params).fetchall()]


def execute(query: str, params: tuple = ()) -> int:
    """Execute a write query. Returns lastrowid."""
    with get_conn() as conn:
        cur = conn.execute(query, params)
        return cur.lastrowid


def execute_many(query: str, params_list: list[tuple]) -> None:
    """Execute a write query against a list of param tuples."""
    with get_conn() as conn:
        conn.executemany(query, params_list)


def table_exists(table_name: str) -> bool:
    """Check whether a table exists in the database."""
    row = fetch_one(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    )
    return row is not None