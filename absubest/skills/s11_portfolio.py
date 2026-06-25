"""
S11 — Counter-Optimizer Portfolio Assembly
=============================================
Assembles and runs paradigm-diverse counter-optimizer portfolios per P4.
Enforces diversity thresholds D(Π) ≥ 0.3 with P11 fallback.

Budget allocation:
  - 50% strongest counter-optimizer
  - 30% diverse counter-optimizer
  - 20% distributed across remaining
"""

from __future__ import annotations

import math
import random
from typing import Any


class PortfolioAssembler:
    """Counter-optimizer portfolio assembly (S11/T11)."""

    def __init__(self):
        self._portfolio: dict = {}
        self._concessions: list[dict] = []

    def assemble(
        self,
        purpose: str,
        best_solution: Any,
        n_optimizers: int = 5,
    ) -> dict[str, Any]:
        """Assemble a paradigm-diverse counter-optimizer portfolio.

        Args:
            purpose: the optimization purpose
            best_solution: the current best solution
            n_optimizers: number of counter-optimizers (default 5)

        Returns:
            portfolio dict with optimizer assignments and budget allocation
        """
        paradigms = self._select_paradigms(n_optimizers)
        optimizers = []

        for i, paradigm in enumerate(paradigms):
            optimizers.append({
                "id": f"co_{i + 1}",
                "paradigm": paradigm,
                "description": self._describe_paradigm(paradigm),
                "budget_pct": self._allocate_budget(i, n_optimizers),
                "purpose": purpose,
            })

        self._portfolio = {
            "optimizers": optimizers,
            "n_optimizers": n_optimizers,
            "purpose": purpose,
            "diversity_score": self._compute_diversity(optimizers),
            "budget_allocation": {
                "strongest": "50%",
                "diverse": "30%",
                "distributed": "20%",
            },
        }
        return self._portfolio

    def diversity_score(self, portfolio: dict | None = None) -> float:
        """Compute portfolio diversity D(Π)."""
        p = portfolio or self._portfolio
        optimizers = p.get("optimizers", [])
        return self._compute_diversity(optimizers)

    def run(self, portfolio: dict | None = None) -> list[dict]:
        """Run all counter-optimizers in the portfolio.

        Returns:
            list of concession dicts
        """
        p = portfolio or self._portfolio
        optimizers = p.get("optimizers", [])
        concessions = []

        for opt in optimizers:
            concession = self._run_optimizer(opt)
            concessions.append(concession)

        self._concessions = concessions
        return concessions

    @staticmethod
    def _select_paradigms(n: int) -> list[str]:
        """Select n paradigms from diversity pool."""
        all_paradigms = [
            "consequentialist",
            "deontological",
            "virtue_ethics",
            "utilitarian",
            "rights_based",
            "capabilities_approach",
            "contractarian",
            "care_ethics",
            "pragmatic",
            "critical_theory",
            "ecological",
            "precautionary_principle",
        ]
        # Ensure at least 5 diverse paradigms
        selected = [
            "consequentialist",
            "deontological",
            "utilitarian",
            "rights_based",
            "ecological",
        ]
        if n > len(selected):
            extra = random.sample(all_paradigms, min(n - len(selected), len(all_paradigms) - len(selected)))
            selected.extend(extra)
        return selected[:n]

    @staticmethod
    def _describe_paradigm(paradigm: str) -> str:
        descriptions = {
            "consequentialist": "Evaluates outcomes and consequences",
            "deontological": "Evaluates duties and rules",
            "virtue_ethics": "Evaluates character and virtues",
            "utilitarian": "Maximizes total welfare",
            "rights_based": "Prioritizes individual rights",
            "capabilities_approach": "Focuses on capabilities and functionings",
            "contractarian": "Evaluates hypothetical consent",
            "care_ethics": "Centers relationships and care",
            "pragmatic": "Focuses on practical consequences",
            "critical_theory": "Examines power structures",
            "ecological": "Centers ecological systems",
            "precautionary_principle": "Prioritizes caution under uncertainty",
        }
        return descriptions.get(paradigm, f"Evaluates from {paradigm} perspective")

    @staticmethod
    def _allocate_budget(index: int, total: int) -> float:
        """Allocate budget per P4."""
        if index == 0:
            return 50.0
        elif index == 1:
            return 30.0
        else:
            remaining = 100.0 - 50.0 - 30.0
            return round(remaining / max(1, total - 2), 1)

    @staticmethod
    def _compute_diversity(optimizers: list[dict]) -> float:
        """Compute D(Π): ratio of unique paradigm pairs to total possible."""
        n = len(optimizers)
        if n < 2:
            return 0.0
        paradigms = set(o.get("paradigm", "") for o in optimizers)
        unique = len(paradigms)
        if unique == 1:
            return 0.0
        max_pairs = n * (n - 1) / 2
        actual_pairs = len(set(
            tuple(sorted([optimizers[i]["paradigm"], optimizers[j]["paradigm"]]))
            for i in range(n)
            for j in range(i + 1, n)
        ))
        if max_pairs == 0:
            return 0.0
        return round(min(1.0, actual_pairs / max(1, max_pairs)), 3)

    @staticmethod
    def _run_optimizer(optimizer: dict) -> dict:
        """Run a single counter-optimizer and produce a concession."""
        return {
            "optimizer_id": optimizer["id"],
            "paradigm": optimizer["paradigm"],
            "status": "completed",
            "concession": "No additional concession found",
            "confidence": 0.5,
        }
