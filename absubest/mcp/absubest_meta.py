"""
MCP-1 Meta-Agent — FastMCP (official MCP Python SDK) over stdio.

The primary MCP server for the ABSUBEST-Exactor. Exposes the full
pipeline as callable tools for integration with LLM agents, editors,
and headless automation.

Tools:
    ping         → {"pong": true, "version": "0.1.0"}
    optimize     → run ABSUBEST pipeline on a purpose
    resume       → resume a previously checkpointed task
    registry_list → list archived declarations
    registry_get  → get a specific declaration by registry_id
    bias_audit    → bias audit for a task_id
    reverify      → trigger re-verification for a registry_id
"""

from __future__ import annotations

import logging
import traceback
from typing import Any

from mcp.server.fastmcp import FastMCP

from absubest.core.orchestrator import ABSUBEST
from absubest.skills.s13_bias import BiasSteward
from absubest.skills.s14_state import StatePersistence
from absubest.skills.s15_registry import ABSUBESTRegistry

logger = logging.getLogger("absubest.mcp")

# Module-level instances (lazy init inside tool functions avoids import-order issues)
_orchestrator: ABSUBEST | None = None
_registry: ABSUBESTRegistry | None = None
_state: StatePersistence | None = None
_bias: BiasSteward | None = None


def _get_orchestrator() -> ABSUBEST:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ABSUBEST()
    return _orchestrator


def _get_registry() -> ABSUBESTRegistry:
    global _registry
    if _registry is None:
        _registry = ABSUBESTRegistry()
    return _registry


def _get_state() -> StatePersistence:
    global _state
    if _state is None:
        _state = StatePersistence()
    return _state


def _get_bias() -> BiasSteward:
    global _bias
    if _bias is None:
        _bias = BiasSteward()
    return _bias


mcp = FastMCP(
    "absubest-meta",
    instructions="ABSUBEST MCP-1 Meta-Agent Server — exposes the ABSUBEST pipeline as MCP tools",
)


# ── Tools ────────────────────────────────────────────────────────────────────


@mcp.tool()
def ping() -> dict:
    """Health-check the ABSUBEST MCP server.

    Returns:
        A dict with ``pong`` (always ``True``) and the server ``version``.
    """
    from absubest import __version__

    return {"pong": True, "version": __version__}


@mcp.tool()
def optimize(
    purpose: str,
    context: dict | None = None,
    odi_override: float | None = None,
) -> dict:
    """Run the ABSUBEST optimisation pipeline for a given purpose.

    Delegates to :class:`absubest.core.orchestrator.ABSUBEST`.

    Args:
        purpose: Human-readable purpose statement for the optimisation.
        context: Optional dict of contextual parameters.
        odi_override: Optional float to override the ODi (Optimal Design Index).

    Returns:
        The result dict emitted by the ABSUBEST pipeline.

    Raises:
        ValueError: If ``purpose`` is missing or not a string.
    """
    if not purpose or not isinstance(purpose, str):
        raise ValueError("Missing / invalid 'purpose' (required string)")
    try:
        result = _get_orchestrator().optimize(purpose, context, odi_override)
        return result
    except Exception:
        logger.exception("optimize failed for purpose=%r", purpose)
        raise


@mcp.tool()
def resume(task_id: str) -> dict:
    """Resume a previously checkpointed ABSUBEST task.

    Delegates to :class:`absubest.skills.s14_state.StatePersistence`.

    Args:
        task_id: The unique identifier of the task to resume.

    Returns:
        A dict with ``task_id`` and ``state`` (or ``None`` if no saved state).

    Raises:
        ValueError: If ``task_id`` is empty.
        LookupError: If no saved state exists for ``task_id``.
    """
    if not task_id:
        raise ValueError("Missing required parameter 'task_id'")
    try:
        state = _get_state().resume(task_id)
    except Exception:
        logger.exception("resume failed for task_id=%r", task_id)
        raise
    if state is None:
        return {"task_id": task_id, "state": None, "note": "No saved state found for this task_id"}
    return {"task_id": task_id, "state": state}


@mcp.tool()
def registry_list() -> dict:
    """List all archived declarations in the registry.

    Delegates to :class:`absubest.skills.s15_registry.ABSUBESTRegistry`.

    Returns:
        A dict with an ``entries`` list and a ``count`` integer.
    """
    try:
        entries = _get_registry().list_declarations()
        return {"entries": entries, "count": len(entries)}
    except Exception:
        logger.exception("registry_list failed")
        raise


@mcp.tool()
def registry_get(registry_id: str) -> dict:
    """Get a specific declaration from the registry by its ID.

    Delegates to :class:`absubest.skills.s15_registry.ABSUBESTRegistry`.

    Args:
        registry_id: The unique identifier of the declaration.

    Returns:
        The declaration entry as a dict.

    Raises:
        ValueError: If ``registry_id`` is empty.
        LookupError: If the declaration is not found.
    """
    if not registry_id:
        raise ValueError("Missing required parameter 'registry_id'")
    try:
        entry = _get_registry().lookup(registry_id)
    except Exception:
        logger.exception("registry_get failed for registry_id=%r", registry_id)
        raise
    if entry is None:
        raise LookupError(f"Declaration not found: {registry_id}")
    return entry


@mcp.tool()
def bias_audit(task_id: str) -> dict:
    """Run a bias audit on a completed ABSUBEST task.

    Delegates to :class:`absubest.skills.s13_bias.BiasSteward`.

    Args:
        task_id: The unique identifier of the task to audit.

    Returns:
        A dict with ``task_id`` and ``audit`` (the audit result).

    Raises:
        ValueError: If ``task_id`` is empty.
    """
    if not task_id:
        raise ValueError("Missing required parameter 'task_id'")
    try:
        audit = _get_bias().audit(task_id)
        return {"task_id": task_id, "audit": audit}
    except Exception:
        logger.exception("bias_audit failed for task_id=%r", task_id)
        raise


@mcp.tool()
def reverify(registry_id: str) -> dict:
    """Trigger a re-verification for a previously registered declaration.

    Looks up the declaration in the registry, extracts its original
    ``purpose``, and feeds it back through the ABSUBEST pipeline.

    Delegates to :class:`absubest.skills.s15_registry.ABSUBESTRegistry` and
    :class:`absubest.core.orchestrator.ABSUBEST`.

    Args:
        registry_id: The unique identifier of the declaration to re-verify.

    Returns:
        A dict with ``registry_id`` and ``result`` (the pipeline result).

    Raises:
        ValueError: If ``registry_id`` is empty.
        LookupError: If the declaration is not found or has no purpose.
    """
    if not registry_id:
        raise ValueError("Missing required parameter 'registry_id'")
    try:
        entry = _get_registry().lookup(registry_id)
    except Exception:
        logger.exception("reverify lookup failed for registry_id=%r", registry_id)
        raise
    if entry is None:
        raise LookupError(f"Declaration not found: {registry_id}")
    purpose = entry.get("purpose", "")
    if not purpose:
        raise LookupError("Declaration has no purpose field for re-verification")
    try:
        # Re-run with original purpose; re-verification flag tracked in metadata
        result = _get_orchestrator().optimize(
            purpose,
            odi_weights="default",
            task_id=f"reverify-{registry_id}",
        )
        return {"registry_id": registry_id, "result": result}
    except Exception:
        logger.exception("reverify optimisation failed for registry_id=%r", registry_id)
        raise


# ── Entry point ──────────────────────────────────────────────────────────────


def main() -> None:
    """Run the ABSUBEST MCP-1 Meta-Agent server over stdio."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(name)s | %(message)s",
    )
    logger.info("Starting ABSUBEST MCP-1 Meta-Agent (FastMCP / stdio)")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
