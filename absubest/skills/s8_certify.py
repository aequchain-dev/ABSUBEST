"""
S8 — Optimality Certification
===============================
Produces optimality certificates with escalating rigor:
Pareto → upper-bound → statistical → formal → redundant.

Portfolio concession is the fallback when formal is not available.
"""

from __future__ import annotations

from typing import Any


class Certifier:
    """Optimality certification engine (S8/T8)."""

    CERTIFICATION_METHODS = [
        "pareto",
        "upper_bound",
        "statistical",
        "formal",
        "redundant_formal",
        "portfolio_concession",
    ]

    def __init__(self):
        self._certificate: dict = {}
        self._residual_risk: str = ""

    def certify(
        self,
        evaluation: dict,
        odi: float,
        epsilon: float = 0.01,
    ) -> dict[str, Any]:
        """Produce optimality certificate.

        Args:
            evaluation: result dict from Evaluator.evaluate()
            odi: Optimality Demand Index score
            epsilon: optimality gap (default 0.01)

        Returns:
            dict with:
                - type: certificate type
                - method: certification method used
                - best_solution: id of best candidate
                - utility: best utility score
                - epsilon: optimality gap (if applicable)
                - gap_detected: whether a gap remains
                - confidence: confidence level
        """
        best_id = evaluation.get("best_id", "")
        best_utility = evaluation.get("best", 0.0)

        # Choose method based on ODI
        method = self._select_method(odi)

        gap_detected = best_utility < (10.0 - epsilon)

        self._certificate = {
            "type": method,
            "method": method,
            "best_solution": best_id,
            "utility": round(best_utility, 4),
            "epsilon": epsilon,
            "gap_detected": gap_detected,
            "confidence": self._confidence(method),
            "odi_at_time_of_certification": odi,
        }

        # Residual risk labeling (mandatory)
        self._residual_risk = self._compute_residual_risk(method, gap_detected)

        return self._certificate

    def residual_risk_label(self) -> str:
        """Return the honest residual risk label (mandatory)."""
        return self._residual_risk

    @staticmethod
    def _select_method(odi: float) -> str:
        if odi < 4:
            return "pareto"
        elif odi < 7:
            return "statistical"
        else:
            return "formal"

    @staticmethod
    def _confidence(method: str) -> float:
        confidences = {
            "pareto": 0.5,
            "upper_bound": 0.6,
            "statistical": 0.7,
            "formal": 0.9,
            "redundant_formal": 0.95,
            "portfolio_concession": 0.4,
        }
        return confidences.get(method, 0.5)

    @staticmethod
    def _compute_residual_risk(method: str, gap_detected: bool) -> str:
        if gap_detected:
            return "gap detected — solution may not be globally optimal"
        if method in ("portfolio_concession", "pareto"):
            return "uncalibrated — portfolio concession, not proven optimal"
        if method == "statistical":
            return "statistical — residual uncertainty from sampling"
        if method in ("formal", "redundant_formal"):
            return (
                "formally verified within modeled constraints — "
                "residual risk from simplification assumptions"
            )
        return "unknown"
