"""
S13 — Bias Steward
====================
Bias detection, correction, and veto (P5 + P14 self-application correction).
"""

from __future__ import annotations

from typing import Any


class BiasSteward:
    """Bias detection and correction (S13/T13)."""

    KNOWN_BIASES = {
        "availability": "Overweighting recent or memorable examples",
        "confirmation": "Seeking evidence that confirms existing beliefs",
        "anchoring": "Over-relying on first piece of information",
        "framing": "Being swayed by presentation rather than substance",
        "optimism": "Overestimating positive outcomes",
        "overconfidence": "Overestimating one's own abilities or knowledge",
        "selection": "Biased sample selection",
        "survivorship": "Focusing on successes, ignoring failures",
        "sunk_cost": "Continuing due to past investment",
        "groupthink": "Conforming to group consensus",
        "authority": "Overvaluing opinions of authority figures",
        "dimensional": "Neglecting relevant evaluation dimensions",
    }

    def __init__(self):
        self._audit_log: list[dict] = []
        self._correction_budget: int = 80  # default P5 budget

    def audit(
        self,
        task_id: str,
        scores: dict | None = None,
        purpose: str | None = None,
    ) -> list[dict]:
        """Run bias audit on the current evaluation.

        Returns:
            list of bias findings
        """
        findings = []

        for bias_name, description in self.KNOWN_BIASES.items():
            likely, severity = self._detect_bias(bias_name, scores)
            if likely:
                findings.append({
                    "bias": bias_name,
                    "description": description,
                    "severity": severity,
                    "mitigation": self._mitigation(bias_name),
                })

        self._audit_log = findings
        return findings

    def apply_correction(self, bias_name: str) -> dict[str, Any]:
        """Apply P5 correction budget to a specific bias."""
        if self._correction_budget <= 0:
            return {"status": "budget_exhausted", "bias": bias_name}

        self._correction_budget -= 20
        return {
            "status": "corrected",
            "bias": bias_name,
            "correction_applied": self._mitigation(bias_name),
            "remaining_budget": self._correction_budget,
        }

    def veto(self, bias_name: str) -> dict[str, Any]:
        """Veto a result due to uncorrectable bias."""
        return {
            "status": "veto",
            "bias": bias_name,
            "reason": f"Uncorrectable bias detected: {bias_name}",
        }

    @staticmethod
    def _detect_bias(bias_name: str, scores: dict | None = None) -> tuple[bool, str]:
        """Detect if a bias is likely present."""
        likely_biases = {
            "availability": (False, "low"),
            "confirmation": (False, "low"),
            "anchoring": (False, "low"),
            "framing": (True, "low"),       # always present in language-based evaluation
            "optimism": (True, "medium"),
            "overconfidence": (True, "medium"),
            "selection": (False, "low"),
            "survivorship": (False, "low"),
            "sunk_cost": (False, "low"),
            "groupthink": (False, "low"),
            "authority": (False, "low"),
            "dimensional": (False, "low"),
        }
        return likely_biases.get(bias_name, (False, "low"))

    @staticmethod
    def _mitigation(bias_name: str) -> str:
        mitigations = {
            "availability": "Use systematic sampling, not recent examples",
            "confirmation": "Actively seek disconfirming evidence",
            "anchoring": "Consider multiple reference points",
            "framing": "Reframe the decision in multiple ways",
            "optimism": "Apply reference class forecasting",
            "overconfidence": "Calibrate confidence intervals",
            "selection": "Ensure random or stratified sampling",
            "survivorship": "Include failures in analysis",
            "sunk_cost": "Evaluate forward-looking only",
            "groupthink": "Assign devil's advocate role",
            "authority": "Blind evaluation where possible",
            "dimensional": "Systematically expand dimension set",
        }
        return mitigations.get(bias_name, "Document and disclose")


def bias_check(dimension: str) -> str:
    """Quick bias type lookup for a dimension (used by DimensionDeriver)."""
    bias_map = {
        "performance": "availability — recent performance often overweights",
        "cost": "anchoring — first cost estimate anchors decisions",
        "safety": "optimism — safety risks are systematically underestimated",
        "fairness": "confirmation — existing fairness beliefs persist",
        "sustainability": "framing — short-term vs long-term framing matters",
        "usability": "selection — power users not representative",
    }
    return bias_map.get(dimension, f"framing — disclosure recommended")
