"""
Meta-Calibrator — Layer 0
===========================
Computes ODI, generates task blueprints, and calibrates pipeline rigor.

Invoked by the Orchestrator before any stage execution.
"""

from __future__ import annotations

from typing import Any, Optional


class MetaCalibrator:
    """Layer 0 meta-control: compute ODI, generate blueprint, declare coverage class."""

    def __init__(self):
        self.purpose: str = ""
        self.context: dict = {}

    def odi_precheck(
        self,
        purpose: str,
        context: dict,
        stakeholders: list[str] | None = None,
    ) -> dict[str, Any]:
        """Run the 5-question ODI Pre-Check (P1).

        Returns:
            dict with answers, mandatory floors, routing, coverage class
        """
        from absubest.skills.s1_odi_precheck import odi_precheck

        self.purpose = purpose
        self.context = context
        return odi_precheck(purpose, context, stakeholders or [])

    def compute_odi(
        self,
        precheck_result: dict,
        weight_profile: str = "default",
    ) -> float:
        """Compute ODI score from pre-check results."""
        harm = precheck_result.get("harm_check", False)
        scale = precheck_result.get("scale_check", False)
        reversible = precheck_result.get("reversible_check", True)

        w_I = 5 if not reversible else 1
        w_B = 2 if scale else 1
        w_M = 2 if harm else 1
        w_C = 0.5

        # Normalize to 0-10 scale
        raw = float(w_I + w_B + w_M + w_C) / (5 + 2 + 2 + 0.5) * 10
        odi = min(10.0, max(0.0, raw))
        return round(odi, 2)

    def generate_blueprint(
        self,
        odi: float,
        coverage_class: str,
    ) -> dict[str, Any]:
        """Generate task-specific blueprint with stage selection and rigor."""
        if odi < 4:
            pipeline = "lite"
            stages = ["A", "D", "E", "F", "H"]
        elif odi < 7:
            pipeline = "express"
            stages = ["A", "B", "C", "D", "E", "F", "H"]
        else:
            pipeline = "full"
            stages = ["A", "B", "C", "D", "E", "F", "G", "H"]

        return {
            "odi": odi,
            "pipeline": pipeline,
            "coverage_class": coverage_class,
            "stages": stages,
            "tier": 1 if odi < 4 else (2 if odi < 7 else 4),
            "fast_track": odi < 4,
            "counter_optimization_required": odi >= 7,
            "moral_screens_required": True,
            "bias_correction_budget": 80 if odi >= 7 else 0,
        }

    def declare_coverage_class(self, purpose: str, context: dict) -> str:
        """Declare coverage class: computable or heuristic."""
        characterizable = self._is_characterizable(purpose)
        return "computable" if characterizable else "heuristic"

    @staticmethod
    def _is_characterizable(purpose: str) -> bool:
        """Heuristic: is the solution space formally characterizable?"""
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
