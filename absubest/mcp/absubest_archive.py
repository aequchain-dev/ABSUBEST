"""
MCP-4 Declaration Archive — FastMCP over stdio.

Persists, queries, compares, and manages ABSUBEST declarations with
SHA-256 comparability headers (P13). Delegates persistence to
ABSUBESTRegistry (s15_registry). Actual API:

    ABSUBESTRegistry.archive(result: ABSUBESTResult) -> str
    ABSUBESTRegistry.lookup(task_id: str) -> dict | None
    ABSUBESTRegistry.list_declarations(limit: int) -> list[dict]
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

from absubest.core.orchestrator import ABSUBESTResult
from absubest.skills.s15_registry import ABSUBESTRegistry

mcp = FastMCP(
    name="absubest-archive",
    instructions="ABSUBEST MCP-4 Declaration Archive Server",
)

_registry = ABSUBESTRegistry()


def _compute_comparability_header(declaration: dict) -> str:
    """P13: Compute SHA-256 comparability header of canonical JSON."""
    canonical = json.dumps(declaration, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _build_result(**kw: dict) -> ABSUBESTResult:
    """Build an ABSUBESTResult dataclass from keyword args, filling defaults."""
    defaults = dict(
        purpose="",
        solution=None,
        utility=0.0,
        certificate="",
        certificate_method="",
        residual_risk="",
        declaration="",
        moral_screens={},
        odi_score=0.0,
        comparability_header={},
        expiration_date="",
        reverification_triggers=[],
        p11_tier=None,
        bias_audit=None,
        solution_text="",
        task_id=f"reg-{int(time.time())}",
    )
    defaults.update(kw)
    return ABSUBESTResult(**defaults)


@mcp.tool()
def ping() -> dict:
    """Health check."""
    return {"pong": True, "server": "absubest-archive"}


@mcp.tool()
def archive_store(
    declaration: dict, purpose: str = "", framework_version: str = ""
) -> dict:
    """Store a declaration in the registry.

    Args:
        declaration: The full declaration document.
        purpose: Purpose for indexing.
        framework_version: Version string (default '3.1').
    """
    if not declaration:
        raise ValueError("Missing/invalid 'declaration' (required dict)")

    resolved_purpose = purpose or declaration.get("purpose", "unknown")
    resolved_version = framework_version or "3.1"

    comparability_hash = _compute_comparability_header(declaration)

    decl_id = f"reg-{int(time.time())}"
    now_iso = datetime.now(timezone.utc).isoformat()

    # Build ABSUBESTResult dataclass as required by registry.archive()
    result = _build_result(
        task_id=decl_id,
        purpose=resolved_purpose,
        declaration=json.dumps(declaration, default=str),
        comparability_header={"_sha256": comparability_hash, "_version": resolved_version},
        odi_score=declaration.get("odi_computed", declaration.get("odi", 0.0)),
        moral_screens=declaration.get("moral_screens", {"p6": "pass", "p6b": "pass"}),
        certificate_method=declaration.get("certificate_method", ""),
        residual_risk=declaration.get("residual_risk_label", ""),
        expiration_date=declaration.get("expires_at", ""),
        utility=declaration.get("utility", declaration.get("utility_score", 0.0)),
    )

    reg_id = _registry.archive(result)
    return {
        "declaration_id": reg_id,
        "comparability_header": comparability_hash,
        "stored": True,
    }


@mcp.tool()
def archive_get(declaration_id: str) -> dict:
    """Retrieve a declaration by ID.

    Args:
        declaration_id: The declaration identifier.
    """
    if not declaration_id:
        raise ValueError("Missing/invalid 'declaration_id' (required string)")

    declaration = _registry.lookup(declaration_id)
    if declaration is None:
        raise ValueError(f"Declaration not found: {declaration_id}")

    return {
        "declaration_id": declaration_id,
        "declaration": declaration,
        "has_comparability": bool(declaration.get("comparability_header")),
    }


@mcp.tool()
def archive_list(
    purpose: str = "",
    framework_version: str = "",
    limit: int = 20,
    offset: int = 0,
) -> dict:
    """List declarations with optional filters.

    Args:
        purpose: Filter by purpose substring.
        framework_version: Filter by version.
        limit: Max results (default 20).
        offset: Pagination offset (default 0).
    """
    declarations = _registry.list_declarations(limit=min(limit, 100))

    # Apply in-memory filters since list_declarations doesn't support them
    if purpose:
        declarations = [d for d in declarations if purpose.lower() in d.get("purpose", "").lower()]
    if framework_version:
        declarations = [d for d in declarations if d.get("comparability_header", "").find(framework_version) >= 0]

    return {
        "declarations": declarations[offset:],
        "count": len(declarations[offset:]),
        "limit": limit,
        "offset": offset,
    }


@mcp.tool()
def archive_search(query: str, limit: int = 10) -> dict:
    """Search declarations by text via raw SQL.

    Args:
        query: Search string.
        limit: Max results (default 10).
    """
    if not query:
        raise ValueError("Missing/invalid 'query' (required string)")

    # Direct SQL search — registry has no search() method
    import os, tempfile
    db_path = os.path.join(os.environ.get("HOME", tempfile.gettempdir()), ".absubest", "registry.db")
    results = []
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT id, purpose, odi, utility, created_at FROM declarations "
                "WHERE purpose LIKE ? OR declaration_text LIKE ? ORDER BY created_at DESC LIMIT ?",
                (f"%{query}%", f"%{query}%", min(limit, 100)),
            ).fetchall()
            results = [dict(r) for r in rows]
    except Exception:
        pass

    return {
        "results": results,
        "count": len(results),
        "query": query,
    }


@mcp.tool()
def archive_compare(declaration_a: dict, declaration_b: dict) -> dict:
    """Compare two declarations via their comparability headers.

    Args:
        declaration_a: First declaration.
        declaration_b: Second declaration.
    """
    if not declaration_a or not declaration_b:
        raise ValueError("Missing 'declaration_a' and/or 'declaration_b' (required dicts)")

    hash_a = _compute_comparability_header(declaration_a)
    hash_b = _compute_comparability_header(declaration_b)

    purpose_a = declaration_a.get("purpose", declaration_a.get("_purpose", "unknown"))
    purpose_b = declaration_b.get("purpose", declaration_b.get("_purpose", "unknown"))

    differing_fields = []
    all_keys = set(list(declaration_a.keys()) + list(declaration_b.keys()))
    for key in all_keys:
        if key.startswith("_"):
            continue
        if declaration_a.get(key) != declaration_b.get(key):
            differing_fields.append(key)

    return {
        "hash_a": hash_a,
        "hash_b": hash_b,
        "identical": hash_a == hash_b,
        "purpose_a": purpose_a,
        "purpose_b": purpose_b,
        "n_differing_fields": len(differing_fields),
        "differing_fields_sample": differing_fields[:10],
        "is_cross_framework": declaration_a.get("_framework") != declaration_b.get("_framework"),
    }


@mcp.tool()
def archive_delete(declaration_id: str) -> dict:
    """Delete a declaration from the registry via raw SQL.

    Args:
        declaration_id: The declaration identifier.
    """
    if not declaration_id:
        raise ValueError("Missing/invalid 'declaration_id' (required string)")

    import os, tempfile
    db_path = os.path.join(os.environ.get("HOME", tempfile.gettempdir()), ".absubest", "registry.db")
    deleted = False
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.execute("DELETE FROM declarations WHERE id = ?", (declaration_id,))
            deleted = cur.rowcount > 0
            conn.execute("DELETE FROM reverification_triggers WHERE declaration_id = ?", (declaration_id,))
            conn.commit()
    except Exception:
        pass

    return {
        "declaration_id": declaration_id,
        "deleted": deleted,
        "found": deleted,
    }


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
