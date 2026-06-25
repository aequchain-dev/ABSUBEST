"""
S1 — ODI Pre-Check
====================
P1-mandated pre-check: five questions to determine ODI tier.
Supports routing: Lite (ODI < 4), Express (4–6), Full (7–10).
"""

from __future__ import annotations

from typing import Any


def odi_precheck(
    purpose: str,
    context: dict[str, Any],
    stakeholders: list[str] | None = None,
) -> dict[str, Any]:
    """Run the ODI Pre-Check (P1).

    Returns:
        dict with:
          - answers to 5 questions
          - routing: 'lite' | 'express' | 'full'
          - coverage_class: 'computable' | 'heuristic'
          - weights with justification
    """
    if stakeholders is None:
        stakeholders = []

    # ---- 5 questions ----
    questions = {
        "Q1_harm_potential": _q_harm_potential(purpose),
        "Q2_scale_of_impact": _q_scale_of_impact(context),
        "Q3_reversibility": _q_reversibility(context),
        "Q4_stakeholder_diversity": _q_stakeholder_diversity(stakeholders),
        "Q5_characterizability": _q_characterizability(purpose),
    }

    # ---- Compute ODI from pre-check ----
    harm = questions["Q1_harm_potential"]
    scale = questions["Q2_scale_of_impact"]
    reversible = questions["Q3_reversibility"]
    diversity = questions["Q4_stakeholder_diversity"]
    characterizable = questions["Q5_characterizability"]

    w_I = 5 if not reversible else 1
    w_B = 2 if scale >= 7 else 1
    w_M = 2 if harm >= 7 else 1
    w_D = 1 + (diversity - 1) * 0.5  # 1-5 stakeholders -> 1-3 weight

    raw = float(w_I + w_B + w_M + w_D) / (5 + 2 + 2 + 3) * 10
    odi = min(10.0, max(0.0, raw))

    # ---- Routing ----
    if odi < 4:
        routing = "lite"
    elif odi < 7:
        routing = "express"
    else:
        routing = "full"

    # ---- Coverage class ----
    coverage_class = "computable" if characterizable else "heuristic"

    # ---- Weight justification ----
    weight_justification = {
        "w_I (irreversibility)": w_I,
        "w_B (breadth)": w_B,
        "w_M (magnitude of harm)": w_M,
        "w_D (diversity)": round(w_D, 2),
        "justification": (
            "Weights per P1 mandatory floors: irreversibility w_I=5 if not reversible, "
            "breadth w_B=2 if scale>=7, magnitude w_M=2 if harm>=7."
        ),
    }

    return {
        "questions": questions,
        "odi_preliminary": round(odi, 2),
        "routing": routing,
        "coverage_class": coverage_class,
        "weight_justification": weight_justification,
        "stakeholders": stakeholders,
    }


def _q_harm_potential(purpose: str) -> int:
    """Estimate harm potential on 1-10 scale."""
    harm_keywords = {
        "safety": 7,
        "lethal": 10,
        "death": 10,
        "injury": 8,
        "finance": 6,
        "legal": 7,
        "medical": 8,
        "critical": 8,
        "infrastructure": 9,
        "nuclear": 10,
        "weapon": 10,
    }
    pl = purpose.lower()
    scores = [v for k, v in harm_keywords.items() if k in pl]
    if not scores:
        return 1  # low harm
    return max(1, min(10, sum(scores) // len(scores) + 1))


def _q_scale_of_impact(context: dict) -> int:
    """Estimate scale of impact on 1-10."""
    scale_map = {
        "household": 1,
        "community": 3,
        "regional": 5,
        "national": 7,
        "global": 9,
        "infrastructure": 10,
    }
    declared = context.get("deployment_scale", "community")
    if declared in scale_map:
        return scale_map[declared]
    return 3


def _q_reversibility(context: dict) -> bool:
    """Is the impact reversible?"""
    declared = context.get("reversible", True)
    if isinstance(declared, bool):
        return declared
    return True


def _q_stakeholder_diversity(stakeholders: list[str]) -> int:
    """Number of distinct stakeholder groups (1-5)."""
    count = len(stakeholders)
    if count == 0:
        return 1
    if count == 1:
        return 2
    if count <= 3:
        return 3
    if count <= 5:
        return 4
    return 5


def _q_characterizability(purpose: str) -> bool:
    """Is the solution space characterizable?"""
    formal_keywords = [
        "algorithm",
        "optimize",
        "minimize",
        "maximize",
        "select",
        "rank",
        "sort",
        "route",
        "schedule",
        "allocate",
        "program",
        "compute",
        "solve",
        "prove",
        "verify",
        "search",
    ]
    pl = purpose.lower()
    return any(kw in pl for kw in formal_keywords)
