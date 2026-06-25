"""
S15 — ABSUBEST Registry
=========================
Archives declarations with P13 comparability headers.
Supports cross-framework comparability.
"""

from __future__ import annotations

import json
import os
import sqlite3
import tempfile
from datetime import datetime, timezone
from typing import Any

from absubest.core.orchestrator import ABSUBESTResult


class ABSUBESTRegistry:
    """Declaration registry (S15/T15)."""

    def __init__(self, db_path: str | None = None):
        if db_path is None:
            db_dir = os.path.join(
                os.environ.get("HOME", tempfile.gettempdir()),
                ".absubest",
            )
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "registry.db")
        self._db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Initialize SQLite schema."""
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS declarations (
                    id TEXT PRIMARY KEY,
                    purpose TEXT,
                    odi REAL,
                    utility REAL,
                    method TEXT,
                    residual_risk TEXT,
                    moral_screens TEXT,
                    comparability_header TEXT,
                    declaration_text TEXT,
                    created_at TEXT,
                    expires_at TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reverification_triggers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    declaration_id TEXT,
                    trigger TEXT,
                    FOREIGN KEY (declaration_id) REFERENCES declarations(id)
                )
            """)

    def archive(self, result: ABSUBESTResult) -> str:
        """Archive a result in the registry.

        Returns:
            registry ID
        """
        registry_id = result.task_id or f"reg-{id(result)}"

        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO declarations
                    (id, purpose, odi, utility, method, residual_risk,
                     moral_screens, comparability_header, declaration_text,
                     created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    registry_id,
                    result.purpose,
                    result.odi_score,
                    result.utility,
                    result.certificate_method,
                    result.residual_risk,
                    json.dumps(result.moral_screens),
                    json.dumps(result.comparability_header),
                    result.declaration,
                    datetime.now(timezone.utc).isoformat(),
                    result.expiration_date,
                ),
            )
            for trigger in result.reverification_triggers:
                conn.execute(
                    "INSERT INTO reverification_triggers (declaration_id, trigger) VALUES (?, ?)",
                    (registry_id, trigger),
                )
        return registry_id

    def lookup(self, task_id: str) -> dict | None:
        """Look up a declaration by task ID."""
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM declarations WHERE id = ?", (task_id,)
            ).fetchone()
            if row is None:
                return None
            return dict(row)

    def list_declarations(self, limit: int = 20) -> list[dict]:
        """List recent declarations."""
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT id, purpose, odi, utility, created_at, expires_at "
                "FROM declarations ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [dict(r) for r in rows]

    def get_reverification_triggers(self, task_id: str) -> list[str]:
        """Get re-verification triggers for a declaration."""
        with sqlite3.connect(self._db_path) as conn:
            rows = conn.execute(
                "SELECT trigger FROM reverification_triggers WHERE declaration_id = ?",
                (task_id,),
            ).fetchall()
            return [r[0] for r in rows]
