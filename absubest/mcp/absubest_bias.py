"""
MCP-6 Bias Steward — FastMCP stdio server.

Manages bias detection, disclosure, correction budget allocation (P5),
bias veto (P14), and self-application correction (P14 self-apply).
Integrates with s13_bias. Actual API on BiasSteward:

    BiasSteward.audit(task_id, scores, purpose) -> list[dict]
    BiasSteward.apply_correction(bias_name) -> dict
    BiasSteward.veto(bias_name) -> dict
"""

from __future__ import annotations

import time
from typing import Any

from mcp.server.fastmcp import FastMCP

from absubest.skills.s13_bias import BiasSteward

server = FastMCP(
    name="absubest-bias",
    instructions="ABSUBEST MCP-6 Bias Steward Server",
)

_steward = BiasSteward()
_correction_log: list[dict] = []
_detected_biases: list[dict] = []


# ── Meta ─────────────────────────────────────────────────────────────────────


@server.tool()
def ping() -> dict:
    """Health check."""
    return {"pong": True, "server": "absubest-bias"}


# ── Bias Detect ──────────────────────────────────────────────────────────────


@server.tool()
def bias_detect(
    content: dict,
    content_type: str = "artifact",
    odi: float = 5.0,
) -> dict:
    """Detect biases in a specification, decision, or pipeline artifact.

    Delegates to BiasSteward.audit() — the only detection API available.
    """
    if not content:
        raise ValueError("Missing/invalid 'content' (required dict)")

    # bias_steward.audit() accepts (task_id, scores, purpose)
    purpose = content.get("purpose") if isinstance(content, dict) else str(content)[:100]
    task_id = content.get("task_id", f"detect-{int(time.time())}")
    scores = content.get("scores", content.get("dimensions", {}))

    biases = _steward.audit(task_id=task_id, scores=scores, purpose=purpose)
    _detected_biases.clear()
    _detected_biases.extend(biases)

    n_critical = sum(1 for b in biases if b.get("severity") in ("high", "critical"))
    total_score = len(biases)
    threshold_breach = odi >= 7 and total_score > 0

    return {
        "biases": biases,
        "n_detected": len(biases),
        "n_critical": n_critical,
        "total_bias_score": total_score,
        "odi": odi,
        "correction_recommended": threshold_breach or n_critical > 0,
        "content_type": content_type,
    }


# ── Bias Disclose ────────────────────────────────────────────────────────────


@server.tool()
def bias_disclose(
    biases: list[dict] | None = None,
    odi: float = 5.0,
) -> dict:
    """Generate a bias disclosure statement."""
    resolved = biases if biases else _detected_biases

    if not resolved:
        return {
            "disclosure": "No biases detected. No disclosure required.",
            "n_biases": 0,
            "odi": odi,
            "disclosure_length": 0,
        }

    disclosure_lines = [
        f"Bias Disclosure Report (ODI={odi})",
        f"Biases detected: {len(resolved)}",
        "---",
    ]
    for b in resolved:
        desc = b.get("description", b.get("bias", "unknown"))
        sev = b.get("severity", "unknown")
        mitigation = b.get("mitigation", "Document and disclose")
        disclosure_lines.append(f"  - {desc} (severity: {sev})")
        disclosure_lines.append(f"    Mitigation: {mitigation}")

    disclosure = "\n".join(disclosure_lines)

    return {
        "disclosure": disclosure,
        "n_biases": len(resolved),
        "odi": odi,
        "disclosure_length": len(disclosure),
    }


# ── Bias Correction Budget (P5) ──────────────────────────────────────────────


@server.tool()
def bias_correction_budget(
    odi: float = 5.0,
    target_budget: float | None = None,
) -> dict:
    """Allocate/manage P5 correction budget.

    Budget is tracked server-side via _steward.apply_correction()
    calls. Default budget is 80 units, consumed 20 per correction.
    """
    budget_remaining = _steward._correction_budget if hasattr(_steward, '_correction_budget') else 80
    budget_allocated = 80 - budget_remaining

    if target_budget is not None:
        if not 0.0 <= target_budget <= 100.0:
            raise ValueError("'target_budget' must be in [0.0, 100.0]")
        # Setting a target doesn't change actual budget — just a declaration
        target_note = f"User requested budget ≥ {target_budget}"
    else:
        target_note = "No specific target requested"

    budget = {
        "total_budget": 80,
        "allocated": budget_allocated,
        "available_budget": budget_remaining,
        "budget_unit": "points (20 per correction)",
        "max_corrections_possible": budget_remaining // 20,
        "note": target_note,
    }

    p5_violation = odi >= 7 and budget["available_budget"] == 0
    p5_message = None
    if p5_violation:
        p5_message = (
            "P5 VIOLATION: ODI >= 7 requires non-zero correction budget. "
            "Provide 'residual distortion likely' statement or increase budget."
        )

    return {
        "budget": budget,
        "odi": odi,
        "p5_violation": p5_violation,
        "p5_message": p5_message,
    }


# ── Bias Apply Correction ────────────────────────────────────────────────────


@server.tool()
def bias_apply_correction(
    bias_id: str = "",
    correction: str = "",
    budget_consumed: float = 1.0,
    artifact: dict | None = None,
) -> dict:
    """Apply a correction to address a detected bias. Delegates to BiasSteward.apply_correction()."""
    if not correction:
        raise ValueError("Missing/invalid 'correction' (required string)")

    resolved_bias_name = bias_id or correction.split()[0].lower()

    result = _steward.apply_correction(resolved_bias_name)

    entry: dict[str, Any] = {
        "bias_id": resolved_bias_name,
        "correction": correction,
        "budget_consumed": budget_consumed,
        "applied_at": time.time(),
        "has_artifact": bool(artifact),
        "steward_result": result,
    }
    _correction_log.append(entry)

    return {
        "correction": entry,
        "n_total_corrections": len(_correction_log),
        "total_budget_consumed": sum(
            c.get("budget_consumed", 0) for c in _correction_log
        ),
    }


# ── Bias Veto (P14) ──────────────────────────────────────────────────────────


@server.tool()
def bias_veto(
    bias_description: str = "",
    severity: str = "critical",
    rationale: str = "",
    vetoed_by: str = "auto",
) -> dict:
    """Issue a P14 bias veto. Delegates to BiasSteward.veto()."""
    if not bias_description:
        raise ValueError("Missing/invalid 'bias_description' (required string)")

    if not rationale:
        raise ValueError("Missing/invalid 'rationale' (required string)")

    resolved_vetoed_by = "bias-steward" if vetoed_by == "auto" else vetoed_by

    steward_result = _steward.veto(bias_description)

    veto = {
        "veto_id": f"veto_{int(time.time())}",
        "bias_description": bias_description,
        "severity": severity,
        "rationale": rationale,
        "vetoed_by": resolved_vetoed_by,
        "issued_at": time.time(),
        "effect": "BLOCKED — further processing halted pending bias resolution",
        "steward_result": steward_result,
    }

    return {
        "veto": veto,
        "propagation_blocked": True,
        "resolution_required": "Remove or correct the bias before re-processing.",
    }


# ── Bias Self-Apply (P14 self-application) ───────────────────────────────────


@server.tool()
def bias_self_apply(
    agent_output: dict,
    odi: float = 5.0,
) -> dict:
    """P14 self-application correction: correct biases in this agent's own outputs."""
    if not agent_output:
        raise ValueError("Missing/invalid 'agent_output' (required dict)")

    purpose = agent_output.get("purpose", str(agent_output)[:100])
    task_id = agent_output.get("task_id", f"self-{int(time.time())}")
    scores = agent_output.get("scores", {})

    biases = _steward.audit(task_id=task_id, scores=scores, purpose=purpose)
    _detected_biases.clear()
    _detected_biases.extend(biases)

    if not biases:
        return {
            "biases_detected": [],
            "n_bias": 0,
            "self_applied": True,
            "message": "No biases detected in agent output.",
        }

    corrections = []
    for bias in biases:
        bias_name = bias.get("bias", "unknown")
        corr_result = _steward.apply_correction(bias_name)
        _correction_log.append({
            "bias_id": bias_name,
            "correction": bias.get("mitigation", f"Applied correction for {bias_name}"),
            "applied_at": time.time(),
            "steward_result": corr_result,
        })
        corrections.append({
            "bias": bias_name,
            "mitigation": bias.get("mitigation", ""),
            "status": corr_result.get("status", "corrected"),
        })

    return {
        "biases_detected": biases,
        "n_bias": len(biases),
        "corrections_applied": corrections,
        "n_corrections": len(corrections),
        "self_applied": True,
    }


# ── Bias Report ──────────────────────────────────────────────────────────────


@server.tool()
def bias_report(include_history: bool = False) -> dict:
    """Generate a comprehensive bias report (in-memory, no delegation needed)."""
    report: dict[str, Any] = {
        "detected_biases": _detected_biases,
        "n_detected": len(_detected_biases),
        "n_corrections_logged": len(_correction_log),
    }

    if include_history:
        report["correction_history"] = _correction_log

    return report


# ── Entrypoint ───────────────────────────────────────────────────────────────


def main() -> None:
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
