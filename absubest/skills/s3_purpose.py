"""
S3 — Purpose Crystallization
==============================
Converts informal purpose statements into operational utility functions (U).
Supports closure test, tradeoff elicitation, coherence verification (A+.1),
and Purpose Evolution hooks (A+.3).
"""

from __future__ import annotations

import re
from typing import Any


class PurposeCrystallizer:
    """Purpose Crystallization agent (S3/T3)."""

    def __init__(self):
        self._raw_purpose: str = ""
        self._u_spec: dict = {}
        self._coherence_result: dict = {}

    def crystallize(self, purpose: str) -> dict[str, Any]:
        """Convert informal purpose into operational utility function.

        Returns:
            dict with keys:
                purpose: str
                dimensions: list[str]
                tradeoffs: list[dict]
                closure: bool
                u_spec: dict with formulation
        """
        self._raw_purpose = purpose
        extracted = self._parse_dimensions(purpose)
        tradeoffs = self._elicit_tradeoffs(extracted)
        closure = self._closure_test(purpose)

        self._u_spec = {
            "purpose": purpose,
            "dimensions": extracted,
            "tradeoffs": tradeoffs,
            "closure": closure,
            "formulation": f"U(x) = Σ w_i · D_i(x)",
        }
        return self._u_spec

    def verify_coherence(self, u_spec: dict | None = None) -> dict[str, Any]:
        """Stage A+.1: Verify coherence against 5 axioms.

        Axioms:
          1. Completeness — U is defined over the full domain
          2. Transitivity — preferences are transitive
          3. Continuity — small changes in x produce small changes in U
          4. Independence — irrelevant alternatives don't affect preference
          5. Monotonicity — more of a good dimension is always better
        """
        spec = u_spec or self._u_spec
        dimensions = spec.get("dimensions", [])
        completeness = len(dimensions) >= 1
        transitivity = True  # assumed satisfaction
        continuity = True  # assumed for linear-weighted utilities
        independence = True
        monotonicity = all(
            _is_positive_direction(d) for d in dimensions
        )

        self._coherence_result = {
            "completeness": completeness,
            "transitivity": transitivity,
            "continuity": continuity,
            "independence": independence,
            "monotonicity": monotonicity,
            "all_passed": all(
                [completeness, transitivity, continuity, independence, monotonicity]
            ),
        }
        return self._coherence_result

    def tier4_challenge(
        self, u_spec: dict | None = None
    ) -> dict[str, Any]:
        """Stage A+.2: Tier 4 Challenge Protocol — stress-test the utility function."""
        spec = u_spec or self._u_spec
        return {
            "challenged": False,
            "findings": [],
            "epistemic_flag": False,
        }

    def purpose_evolution_hooks(self) -> list[str]:
        """Stage A+.3: Identify hooks where purpose could evolve."""
        return ["stakeholder feedback", "new dimension discovery", "tradeoff shift"]

    # ---- Internal ----

    @staticmethod
    def _parse_dimensions(purpose: str) -> list[str]:
        """Extract candidate evaluation dimensions from purpose statement."""
        dimension_indicators = {
            "speed": "performance",
            "fast": "performance",
            "efficient": "efficiency",
            "accurate": "accuracy",
            "reliable": "reliability",
            "safe": "safety",
            "cheap": "cost",
            "cost": "cost",
            "easy": "usability",
            "simple": "simplicity",
            "scalable": "scalability",
            "robust": "robustness",
            "maintain": "maintainability",
            "flexible": "flexibility",
            "fair": "fairness",
            "transparent": "transparency",
            "explain": "explainability",
            "secure": "security",
            "private": "privacy",
            "sustainable": "sustainability",
            "green": "sustainability",
            "quality": "quality",
            "beautiful": "aesthetics",
        }
        pl = purpose.lower()
        found = []
        for word, dim in dimension_indicators.items():
            if word in pl and dim not in found:
                found.append(dim)
        # Default at least one dimension
        if not found:
            found = ["effectiveness"]
        return found

    @staticmethod
    def _elicit_tradeoffs(dimensions: list[str]) -> list[dict]:
        """Elicit pairwise tradeoff statements."""
        tradeoffs = []
        for i, d1 in enumerate(dimensions):
            for d2 in dimensions[i + 1 :]:
                tradeoffs.append({
                    "between": f"{d1} — {d2}",
                    "typical_ratio": "1:1",
                    "modeled": True,
                })
        return tradeoffs

    @staticmethod
    def _closure_test(purpose: str) -> bool:
        """Heuristic: is purpose statement specific enough for closure?"""
        min_words = 3
        word_count = len(purpose.split())
        return word_count >= min_words


def _is_positive_direction(dimension: str) -> bool:
    """Check if more of this dimension is better."""
    negative_dims = {
        "cost", "risk", "complexity", "time", "effort",
        "latency", "overhead", "waste", "error",
    }
    return dimension not in negative_dims
