"""
ABSUBEST MCP-5 State Persistence Server — FastMCP implementation.

Checkpoints and resumes macro-tasks across sessions (P12).
Supports saving/loading pipeline state, session metadata,
integrity verification, and lifecycle management (F22, F30).

Tools:
    ping             → health check
    state_save       → Save a checkpoint (task state)
    state_load       → Load a checkpoint by ID
    state_list       → List available checkpoints
    state_delete     → Remove a checkpoint
    state_integrity  → Verify checkpoint integrity
    state_resume     → Get state for resuming from a checkpoint
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from typing import Any

from mcp.server.fastmcp import FastMCP

from absubest.skills.s14_state import StatePersistence

logger = logging.getLogger("absubest.mcp.state")

# ── Server ──────────────────────────────────────────────────────────────────

mcp = FastMCP(
    "absubest-state",
        instructions="ABSUBEST MCP-5 State Persistence Server",
)

# ── Lazy-init globals ───────────────────────────────────────────────────────

_persister: StatePersistence | None = None
_checkpoint_dir: str | None = None


def _get_persister() -> StatePersistence:
    global _persister
    if _persister is None:
        _persister = StatePersistence()
    return _persister


def _get_checkpoint_dir() -> str:
    global _checkpoint_dir
    if _checkpoint_dir is None:
        _checkpoint_dir = os.path.join(
            os.path.dirname(__file__), "..", ".checkpoints"
        )
        os.makedirs(_checkpoint_dir, exist_ok=True)
    return _checkpoint_dir


def _checkpoint_path(session_id: str) -> str:
    safe = session_id.replace("/", "_").replace("\\", "_")
    return os.path.join(_get_checkpoint_dir(), f"{safe}.json")


def _compute_checksum(data: dict) -> str:
    canonical = json.dumps(data, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ── Tools ────────────────────────────────────────────────────────────────────


@mcp.tool()
def ping() -> dict:
    """returns {"pong": true, "server": "absubest-state"}"""
    return {"pong": True, "server": "absubest-state"}


@mcp.tool()
def state_save(session_id: str, state: dict, metadata: dict | None = None) -> dict:
    """Save pipeline state as a checkpoint.

    Args:
        session_id: Unique session identifier.
        state: Full pipeline state to persist.
        metadata: Session metadata (purpose, stage, etc.).
    """
    if not session_id:
        raise ValueError("Missing/invalid 'session_id' (required string)")

    if not state:
        raise ValueError("Missing/invalid 'state' (required dict)")

    if metadata is None:
        metadata = {}

    envelope = {
        "_meta": {
            "session_id": session_id,
            "saved_at": time.time(),
            "checksum": _compute_checksum(state),
            "format_version": "1.0",
            "purpose": metadata.get("purpose", ""),
            "stage": metadata.get("stage", ""),
            "odi": metadata.get("odi", 0.0),
        },
        "state": state,
        "metadata": metadata,
    }

    path = _checkpoint_path(session_id)
    with open(path, "w") as f:
        json.dump(envelope, f, ensure_ascii=False, indent=2, default=str)

    return {
        "session_id": session_id,
        "checkpoint_path": path,
        "saved_at": envelope["_meta"]["saved_at"],
        "checksum": envelope["_meta"]["checksum"],
        "size_bytes": os.path.getsize(path),
    }


@mcp.tool()
def state_load(session_id: str) -> dict:
    """Load a checkpoint by session ID.

    Args:
        session_id: Session identifier to load.
    """
    if not session_id:
        raise ValueError("Missing/invalid 'session_id' (required string)")

    path = _checkpoint_path(session_id)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Checkpoint not found: {session_id}")

    with open(path) as f:
        envelope = json.load(f)

    return {
        "session_id": session_id,
        "state": envelope.get("state", {}),
        "metadata": envelope.get("metadata", {}),
        "meta": envelope.get("_meta", {}),
        "loaded_at": time.time(),
    }


@mcp.tool()
def state_list(limit: int = 20) -> dict:
    """List all available checkpoints.

    Args:
        limit: Maximum results (default 20).
    """
    checkpoints = []
    for fname in sorted(os.listdir(_get_checkpoint_dir()), reverse=True):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(_get_checkpoint_dir(), fname)
        try:
            with open(fpath) as f:
                envelope = json.load(f)
            meta = envelope.get("_meta", {})
            checkpoints.append({
                "session_id": meta.get("session_id", fname[:-5]),
                "saved_at": meta.get("saved_at", 0),
                "purpose": meta.get("purpose", ""),
                "stage": meta.get("stage", ""),
                "odi": meta.get("odi", 0.0),
                "checksum": meta.get("checksum", ""),
                "size_bytes": os.path.getsize(fpath),
            })
        except (json.JSONDecodeError, KeyError):
            checkpoints.append({
                "session_id": fname[:-5],
                "error": "corrupted",
            })

        if len(checkpoints) >= limit:
            break

    return {"checkpoints": checkpoints, "count": len(checkpoints)}


@mcp.tool()
def state_delete(session_id: str) -> dict:
    """Delete a checkpoint.

    Args:
        session_id: Session identifier to delete.
    """
    if not session_id:
        raise ValueError("Missing/invalid 'session_id' (required string)")

    path = _checkpoint_path(session_id)
    if os.path.exists(path):
        os.remove(path)
        return {"session_id": session_id, "deleted": True}
    else:
        return {"session_id": session_id, "deleted": False, "found": False}


@mcp.tool()
def state_integrity(session_id: str) -> dict:
    """Verify checkpoint integrity (F22/F30 prevention).

    Args:
        session_id: Session identifier to verify.
    """
    if not session_id:
        raise ValueError("Missing/invalid 'session_id' (required string)")

    path = _checkpoint_path(session_id)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Checkpoint not found: {session_id}")

    with open(path) as f:
        envelope = json.load(f)

    state = envelope.get("state", {})
    stored_checksum = envelope.get("_meta", {}).get("checksum", "")
    computed_checksum = _compute_checksum(state)

    valid = stored_checksum == computed_checksum
    extra_fields = [k for k in envelope if k not in ("state", "_meta", "metadata")]

    return {
        "session_id": session_id,
        "valid": valid,
        "stored_checksum": stored_checksum,
        "computed_checksum": computed_checksum,
        "has_extra_fields": len(extra_fields) > 0,
        "extra_fields": extra_fields if extra_fields else None,
        "state_size_keys": len(state.keys()) if isinstance(state, dict) else 0,
    }


@mcp.tool()
def state_resume(session_id: str) -> dict:
    """Get resume-friendly representation of a checkpoint.

    Returns a compact state that can be passed to stage executors
    to continue from the point of interruption.

    Args:
        session_id: Session to resume.
    """
    if not session_id:
        raise ValueError("Missing/invalid 'session_id' (required string)")

    path = _checkpoint_path(session_id)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Checkpoint not found: {session_id}")

    with open(path) as f:
        envelope = json.load(f)

    meta = envelope.get("_meta", {})
    state = envelope.get("state", {})
    metadata = envelope.get("metadata", {})

    completed_stages = metadata.get("completed_stages", [])
    last_stage = meta.get("stage", "")

    next_stages = {
        "A": "B",
        "B": "C",
        "C": "D",
        "D": "E",
        "E": "F",
        "F": "G",
        "G": "H",
        "H": "IMMORTALIZE",
    }
    next_stage = next_stages.get(last_stage, "A")

    return {
        "session_id": session_id,
        "purpose": meta.get("purpose", ""),
        "last_stage": last_stage,
        "next_stage": next_stage,
        "completed_stages": completed_stages,
        "odi": meta.get("odi", 0.0),
        "state_keys": list(state.keys()) if isinstance(state, dict) else [],
        "state": state,
        "metadata": metadata,
    }


# ── Entrypoint ───────────────────────────────────────────────────────────────


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
