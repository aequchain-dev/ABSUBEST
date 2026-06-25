"""
S9 — Transcendence
====================
Applies the six transcendence operators to close identified gaps.

Operators:
  OP_COV — expand coverage
  OP_DIM — add/refine dimensions
  OP_CON — relax constraints
  OP_KNO — expand knowledge
  OP_FOR — improve formalization
  OP_SCL — change scale
"""

from __future__ import annotations

from typing import Any


class Transcender:
    """Transcendence engine (S9/T9)."""

    OPERATORS = {
        "OP_COV": "expand coverage",
        "OP_DIM": "add or refine evaluation dimensions",
        "OP_CON": "relax or remove constraints",
        "OP_KNO": "expand knowledge horizon",
        "OP_FOR": "improve formalization rigor",
        "OP_SCL": "change the scale of analysis",
    }

    def __init__(self):
        self._gaps: list[dict] = []
        self._improved: list[dict] | None = None

    def transcend(
        self,
        purpose: str,
        u_spec: dict,
        evaluation: dict,
        certificate: dict,
    ) -> list[dict] | None:
        """Decompose gap sources and apply transcendence operators.

        Args:
            purpose: the original purpose statement
            u_spec: utility specification
            evaluation: evaluation results dict
            certificate: certification result dict

        Returns:
            improved candidate list, or None if no improvement achieved
        """
        self._gaps = self._decompose_gaps(certificate)
        if not self._gaps:
            return None

        improved_candidates = []

        for gap in self._gaps:
            gap_source = gap.get("source", "unknown")
            operator = self._select_operator(gap_source)

            if operator == "OP_COV":
                candidates = self._apply_op_cov(purpose, u_spec, evaluation)
                improved_candidates.extend(candidates)
            elif operator == "OP_DIM":
                candidates = self._apply_op_dim(evaluation)
                improved_candidates.extend(candidates)
            elif operator == "OP_CON":
                candidates = self._apply_op_con(purpose)
                improved_candidates.extend(candidates)
            elif operator == "OP_SCL":
                candidates = self._apply_op_scl(purpose)
                improved_candidates.extend(candidates)

        self._improved = improved_candidates if improved_candidates else None
        return self._improved

    # ---- Gap decomposition ----

    @staticmethod
    def _decompose_gaps(certificate: dict) -> list[dict]:
        """Decompose gap source from certificate."""
        gaps = []
        if certificate.get("gap_detected", False):
            gaps.append({
                "source": "coverage",
                "description": "Coverage gap detected — further candidates may exist",
                "severity": "medium",
            })
            gaps.append({
                "source": "dimension",
                "description": "New dimensions may improve evaluation",
                "severity": "low",
            })
        return gaps

    @staticmethod
    def _select_operator(gap_source: str) -> str:
        mapping = {
            "coverage": "OP_COV",
            "dimension": "OP_DIM",
            "constraint": "OP_CON",
            "knowledge": "OP_KNO",
            "formalization": "OP_FOR",
            "scale": "OP_SCL",
        }
        return mapping.get(gap_source, "OP_COV")

    # ---- Operator implementations ----

    @staticmethod
    def _apply_op_cov(
        purpose: str,
        u_spec: dict,
        evaluation: dict,
    ) -> list[dict]:
        """OP_COV: expand coverage with additional candidates."""
        from absubest.skills.s6_coverage import CoverageGenerator

        cg = CoverageGenerator()
        dimensions = [{"name": d} for d in u_spec.get("dimensions", ["effectiveness"])]
        return cg.generate(purpose, u_spec, dimensions, n_candidates=3)

    @staticmethod
    def _apply_op_dim(evaluation: dict) -> list[dict]:
        """OP_DIM: add or refine evaluation dimensions."""
        return []

    @staticmethod
    def _apply_op_con(purpose: str) -> list[dict]:
        """OP_CON: relax constraints to widen solution space."""
        return []

    @staticmethod
    def _apply_op_scl(purpose: str) -> list[dict]:
        """OP_SCL: change analysis scale."""
        return []
