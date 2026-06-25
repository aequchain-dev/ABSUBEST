"""
S5 — Dimension Derivation + Bias Disclosure
=============================================
Derives evaluation dimensions from U via concept algebra and causal tracing.
Mandatory bias disclosure (C.bias) and bias correction budget (P5).
"""

from __future__ import annotations

from typing import Any


class DimensionDeriver:
    """Derive evaluation dimensions and disclose biases (S5/T5)."""

    def __init__(self):
        self._dimensions: list[dict] = []
        self._biases: list[dict] = []
        self._bias_correction_budget: int = 0

    def derive(self, u_spec: dict) -> list[dict]:
        """Derive evaluation dimensions from utility specification.

        Args:
            u_spec: dict from PurposeCrystallizer.crystallize()

        Returns:
            list of dimension dicts:
              [{name, description, scale, direction, weight, provenance}]
        """
        dimensions = []
        raw_dims = u_spec.get("dimensions", ["effectiveness"])

        for i, dim in enumerate(raw_dims):
            dimensions.append({
                "name": dim,
                "description": self._describe(dim),
                "scale": "1-10",
                "direction": "maximize" if dim not in ("cost", "risk", "time", "effort") else "minimize",
                "weight": round(1.0 / len(raw_dims), 3),
                "provenance": "concept_algebra",
                "tracing": self._causal_trace(dim),
            })

        self._dimensions = dimensions
        return dimensions

    def disclose_biases(self) -> list[dict]:
        """Disclose known biases in dimension selection (C.bias)."""
        from absubest.skills.s13_bias import bias_check

        self._biases = []
        for dim in self._dimensions:
            b = {
                "dimension": dim["name"],
                "bias_type": bias_check(dim["name"]),
                "mitigation": self._bias_mitigation(dim["name"]),
            }
            self._biases.append(b)

        return self._biases

    def set_bias_correction_budget(self, budget: int) -> None:
        """Set P5 bias correction budget (0-100)."""
        self._bias_correction_budget = budget

    def get_bias_correction_budget(self) -> int:
        return self._bias_correction_budget

    def ontology_map(self) -> dict[str, list[str]]:
        """Map derived dimensions to constraint ontology classes."""
        return {
            "performance": ["physical", "logical"],
            "cost": ["economic"],
            "safety": ["physical", "regulatory"],
            "usability": ["social"],
            "fairness": ["social", "regulatory"],
            "sustainability": ["physical", "economic"],
            "scalability": ["temporal", "logical"],
            "robustness": ["physical", "logical"],
            "security": ["physical", "logical", "regulatory"],
            "privacy": ["regulatory", "social"],
        }

    # ---- Internal ----

    @staticmethod
    def _describe(dim: str) -> str:
        descriptions = {
            "performance": "Speed and throughput of the solution",
            "efficiency": "Resource utilization per unit output",
            "accuracy": "Precision and correctness of results",
            "reliability": "Uptime and consistent behavior",
            "safety": "Absence of harm to users and environment",
            "cost": "Total resource expenditure",
            "usability": "Ease of use and learnability",
            "simplicity": "Low complexity and high comprehensibility",
            "scalability": "Ability to handle increased load",
            "robustness": "Graceful degradation under adverse conditions",
            "maintainability": "Ease of modification and extension",
            "flexibility": "Adaptability to changing requirements",
            "fairness": "Equitable outcomes across groups",
            "transparency": "Auditability and explainability",
            "explainability": "Ability to explain decisions",
            "security": "Protection against threats",
            "privacy": "Protection of personal data",
            "sustainability": "Environmental impact across lifecycle",
            "quality": "Overall excellence and craftsmanship",
            "aesthetics": "Visual and experiential appeal",
            "effectiveness": "Ability to achieve the stated purpose",
        }
        return descriptions.get(dim, f"Quality of {dim}")

    @staticmethod
    def _causal_trace(dim: str) -> list[str]:
        """Trace causal paths from dimension to final outcome."""
        traces = {
            "performance": ["throughput → latency → user satisfaction"],
            "cost": ["expenditure → budget → sustainability"],
            "safety": ["risk → hazard → harm prevention"],
            "usability": ["learnability → adoption → effectiveness"],
            "fairness": ["bias → disparity → equity"],
            "sustainability": ["emissions → lifecycle → environmental impact"],
        }
        return traces.get(dim, [f"{dim} → outcome"])

    @staticmethod
    def _bias_mitigation(dim: str) -> str:
        mitigations = {
            "performance": "measure actual throughput, not self-reported",
            "cost": "include total cost of ownership, not just purchase price",
            "safety": "conduct independent safety audit",
            "fairness": "apply P5 bias correction budget",
            "usability": "empirical user testing with diverse sample",
        }
        return mitigations.get(dim, "document assumptions and disclose")
