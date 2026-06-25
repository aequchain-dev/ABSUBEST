"""
S14 — State Persistence
=========================
Checkpoint and resume macro-tasks across sessions (P12).
"""

from __future__ import annotations

import json
import os
import tempfile
import time
from typing import Any


class StatePersistence:
    """State persistence manager (S14/T14)."""

    def __init__(self, state_dir: str | None = None):
        if state_dir is None:
            state_dir = os.path.join(
                os.environ.get("HOME", tempfile.gettempdir()),
                ".absubest",
                "state",
            )
        self._state_dir = state_dir
        os.makedirs(self._state_dir, exist_ok=True)

    def checkpoint(
        self,
        task_id: str,
        state: dict,
        metadata: dict | None = None,
    ) -> str:
        """Save a checkpoint for a task.

        Args:
            task_id: unique task identifier
            state: the state dict to persist
            metadata: optional metadata (purpose, odi_weights, stage)

        Returns:
            path to checkpoint file
        """
        checkpoint = {
            "task_id": task_id,
            "timestamp": time.time(),
            "state": state,
            "metadata": metadata or {},
        }
        path = os.path.join(self._state_dir, f"{task_id}.json")
        with open(path, "w") as f:
            json.dump(checkpoint, f, indent=2)
        return path

    def resume(self, task_id: str) -> dict | None:
        """Resume a previously checkpointed task."""
        path = os.path.join(self._state_dir, f"{task_id}.json")
        if not os.path.exists(path):
            return None
        with open(path) as f:
            return json.load(f)

    def list_checkpoints(self) -> list[dict]:
        """List all available checkpoints."""
        checkpoints = []
        if not os.path.isdir(self._state_dir):
            return checkpoints
        for fname in os.listdir(self._state_dir):
            if fname.endswith(".json"):
                path = os.path.join(self._state_dir, fname)
                with open(path) as f:
                    try:
                        data = json.load(f)
                        checkpoints.append({
                            "task_id": data.get("task_id", fname.replace(".json", "")),
                            "timestamp": data.get("timestamp", 0),
                            "metadata": data.get("metadata", {}),
                        })
                    except (json.JSONDecodeError, OSError):
                        pass
        checkpoints.sort(key=lambda c: c["timestamp"], reverse=True)
        return checkpoints

    def clear(self, task_id: str) -> bool:
        """Delete a checkpoint."""
        path = os.path.join(self._state_dir, f"{task_id}.json")
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
