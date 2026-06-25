"""
S4 — Constraint Ontology
==========================
Classifies constraints into six classes per v3.1 constraint ontology.
Applies liberation protocol (identify which constraints can be relaxed).
Supports B+ Coverage Monotonicity hooks.
"""

from __future__ import annotations

from typing import Any


class ConstraintClassifier:
    """Constraint classification and liberation (S4/T4)."""

    # Six constraint classes per v3.1
    CONSTRAINT_CLASSES = {
        "physical": "Laws of physics / material limits",
        "logical": "Mathematics / formal logic",
        "economic": "Budget / resource / market constraints",
        "regulatory": "Laws / standards / policies",
        "social": "Cultural / behavioral / ethical norms",
        "temporal": "Time / scheduling / deadlines",
    }

    def __init__(self):
        self._classified: list[dict] = []

    def classify(self, analysis_input: dict) -> list[dict]:
        """Classify constraints into six classes.

        Args:
            analysis_input: dict with keys like 'purpose', 'context', 'explicit_constraints'

        Returns:
            list of dicts: [{constraint, class, justification, liberatable}]
        """
        constraints = []
        raw_purpose = analysis_input.get("purpose", "")

        # Parse implicit constraints from purpose
        implicit = self._detect_implicit(raw_purpose)
        constraints.extend(implicit)

        # Parse explicit constraints if provided
        explicit = analysis_input.get("explicit_constraints", [])
        for c in explicit:
            classified = self._classify_single(c)
            constraints.append(classified)

        self._classified = constraints
        return constraints

    def liberation_protocol(self) -> list[dict]:
        """Apply the liberation protocol: identify relaxable constraints."""
        liberated = []
        for c in self._classified:
            if c.get("liberatable", False):
                liberated.append({
                    "constraint": c["constraint"],
                    "class": c["class"],
                    "relaxation_path": c.get("relaxation_path", ""),
                    "risk_if_relaxed": c.get("risk", "low"),
                })
        return liberated

    def coverage_monotonicity_hooks(
        self, constraints: list[dict] | None = None
    ) -> list[str]:
        """B+ Coverage Monotonicity: identify hooks for coverage expansion."""
        items = constraints or self._classified
        hooks = []
        for c in items:
            if c.get("class") in ("economic", "temporal", "social"):
                hooks.append(f"Relax '{c['constraint']}' to expand coverage")
        return hooks

    # ---- Internal ----

    @staticmethod
    def _detect_implicit(purpose: str) -> list[dict]:
        """Detect implicit constraints from purpose language."""
        pl = purpose.lower()
        found = []

        if any(w in pl for w in ["budget", "cost", "cheap", "affordable"]):
            found.append({
                "constraint": "budget limit",
                "class": "economic",
                "justification": "economic language in purpose",
                "liberatable": True,
                "relaxation_path": "increase budget / find funding",
                "risk": "medium",
            })
        if any(w in pl for w in ["time", "fast", "quick", "deadline"]):
            found.append({
                "constraint": "time limit",
                "class": "temporal",
                "justification": "time language in purpose",
                "liberatable": True,
                "relaxation_path": "extend timeline",
                "risk": "low",
            })
        if any(w in pl for w in ["safe", "secure", "regulatory", "compliant"]):
            found.append({
                "constraint": "safety/regulatory requirement",
                "class": "regulatory",
                "justification": "safety/regulatory language in purpose",
                "liberatable": False,
                "relaxation_path": "",
                "risk": "high",
            })
        if any(w in pl for w in ["simple", "easy", "usable"]):
            found.append({
                "constraint": "usability requirement",
                "class": "social",
                "justification": "usability language in purpose",
                "liberatable": True,
                "relaxation_path": "trade usability for capability",
                "risk": "medium",
            })

        return found

    @staticmethod
    def _classify_single(constraint: str) -> dict:
        """Classify a single constraint statement."""
        cl = constraint.lower()
        for cls_name, keywords in CONSTRAINT_KEYWORDS.items():
            if any(kw in cl for kw in keywords):
                return {
                    "constraint": constraint,
                    "class": cls_name,
                    "justification": f"matched keywords for {cls_name}",
                    "liberatable": cls_name in ("economic", "temporal", "social"),
                    "relaxation_path": _relaxation_path(cls_name),
                    "risk": _risk(cls_name),
                }
        return {
            "constraint": constraint,
            "class": "unknown",
            "justification": "could not classify automatically",
            "liberatable": True,
            "relaxation_path": "needs domain analysis",
            "risk": "unknown",
        }


CONSTRAINT_KEYWORDS = {
    "physical": [
        "material", "strength", "weight", "size", "density",
        "temperature", "pressure", "velocity", "acceleration",
    ],
    "logical": [
        "consistency", "soundness", "completeness", "decidability",
        "complexity", "provably", "algorithmic",
    ],
    "economic": [
        "budget", "cost", "funding", "price", "valuable",
        "revenue", "profit", "margin",
    ],
    "regulatory": [
        "law", "regulation", "compliance", "standard", "policy",
        "legal", "permit", "license", "audit",
    ],
    "social": [
        "culture", "norm", "behavior", "preference", "consent",
        "fairness", "bias", "inclusive",
    ],
    "temporal": [
        "deadline", "schedule", "timeline", "duration", "latency",
        "real-time", "before", "within",
    ],
}


def _relaxation_path(class_name: str) -> str:
    paths = {
        "economic": "increase budget / find alternative funding",
        "temporal": "extend timeline / parallelize",
        "social": "behavioral intervention / education",
        "physical": "alternative materials / design",
        "logical": "weaken specification / approximation",
        "regulatory": "variance / exemption (requires authority)",
    }
    return paths.get(class_name, "domain-dependent")


def _risk(class_name: str) -> str:
    risks = {
        "physical": "high",
        "logical": "high",
        "regulatory": "high",
        "economic": "medium",
        "social": "medium",
        "temporal": "low",
    }
    return risks.get(class_name, "unknown")
