"""
ABSUBEST-Exactor Orchestrator
==============================
Main loop that sequences the ABSUBEST pipeline stages per AGENT.md decision sequence.

Operates as:
  Intake → Existential-Risk Check → Moral Screens → ODI Pre-Check → ODI Computation
  → Blueprint Generation → Stage A (Purpose) → Stage B (Constraints) → Stage C (Dimensions)
  → Stage D (Solution-Space) → Stage E (Evaluation) → Stage F (Certification)
  → Counter-Optimization → Stage G (Transcendence) → Stage H (Verification)
  → Post-Declaration
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class ABSUBESTResult:
    """Result of an ABSUBEST optimization run."""

    purpose: str
    solution: Any
    utility: float
    certificate: str
    certificate_method: str
    residual_risk: str
    declaration: str
    moral_screens: dict[str, str]
    odi_score: float
    comparability_header: dict[str, str]
    expiration_date: str
    reverification_triggers: list[str]
    p11_tier: Optional[str]
    bias_audit: Optional[dict]
    solution_text: str = ""
    task_id: str = ""

    def format(self) -> str:
        lines = [
            "═" * 60,
            f"ABSUBEST DECLARATION — {self.task_id or 'adhoc'}",
            "═" * 60,
            f"Purpose:      {self.purpose}",
            f"ODI:          {self.odi_score:.2f}",
            f"U(x*):        {self.utility:.4f}",
            f"Method:       {self.certificate_method}",
            f"Residual:     {self.residual_risk}",
            f"Expires:      {self.expiration_date}",
            "",
            f"Solution:     {self.solution_text or str(self.solution)}",
            "",
            "Moral Screens:",
        ]
        for k, v in self.moral_screens.items():
            lines.append(f"  {k}: {v}")
        lines.append("")
        if self.bias_audit:
            lines.append("Bias Audit:")
            if isinstance(self.bias_audit, list):
                for entry in self.bias_audit:
                    bias_name = entry.get("bias", "?")
                    severity = entry.get("severity", "?")
                    mitigation = entry.get("mitigation", "N/A")
                    lines.append(f"  • {bias_name} [{severity}] — {mitigation}")
            elif isinstance(self.bias_audit, dict):
                for k, v in self.bias_audit.items():
                    lines.append(f"  {k}: {v}")
        lines.append("")
        if self.p11_tier:
            lines.append(f"P11 Tier: {self.p11_tier}")
        lines.append("")
        lines.append("Comparability Header (P13):")
        for k, v in self.comparability_header.items():
            lines.append(f"  {k}: {v}")
        lines.append("")
        lines.append(self.declaration)
        return "\n".join(lines)


@dataclass
class ABSUBESTConfig:
    """Global configuration for an ABSUBEST instance."""

    knowledge_horizon: str = "2026-06-22"
    resource_budget: str = "unlimited"
    time_budget: str = "unlimited"
    task_id: str = ""
    state_persistence: bool = False
    bias_steward_enabled: bool = True
    registry_path: str = "~/.absubest/registry.db"
    llm_backend: str = "auto"


# ---------------------------------------------------------------------------
# ABSUBEST main class
# ---------------------------------------------------------------------------

class ABSUBEST:
    """Main ABSUBEST framework entry point.

    Usage:
        ab = ABSUBEST()
        result = ab.optimize(purpose="find best algorithm for X")
    """

    def __init__(
        self,
        knowledge_horizon: str = "2026-06-22",
        resource_budget: str = "unlimited",
        time_budget: str = "unlimited",
        task_id: str | None = None,
        state_persistence: bool = False,
        bias_steward_enabled: bool = True,
        registry_path: str = "~/.absubest/registry.db",
        llm_backend: str = "auto",
    ):
        self.config = ABSUBESTConfig(
            knowledge_horizon=knowledge_horizon,
            resource_budget=resource_budget,
            time_budget=time_budget,
            task_id=task_id or f"absubest-{uuid.uuid4().hex[:8]}",
            state_persistence=state_persistence,
            bias_steward_enabled=bias_steward_enabled,
            registry_path=registry_path,
            llm_backend=llm_backend,
        )
        self._state: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def optimize(
        self,
        purpose: str,
        odi_weights: str = "default",
        task_id: str | None = None,
    ) -> ABSUBESTResult:
        """Run ABSUBEST on a stated purpose."""
        if task_id:
            self.config.task_id = task_id

        # Step 1-4: Pipeline execution
        # (In Phase 1, the orchestrator delegates to skill modules)

        result = self._execute_pipeline(purpose, odi_weights)
        return result

    def resume(self, task_id: str) -> ABSUBESTResult:
        """Resume a previously checkpointed task."""
        from absubest.skills.s14_state import StatePersistence

        sp = StatePersistence()
        state = sp.resume(task_id)
        if not state:
            raise ValueError(f"No checkpoint found for task {task_id}")

        self._state = state["state"]
        self.config.task_id = task_id
        # Re-run from last completed stage
        purpose = state["metadata"].get("purpose", "")
        odi_weights = state["metadata"].get("odi_weights", "default")
        return self._execute_pipeline(purpose, odi_weights, resume_state=state)

    # ------------------------------------------------------------------
    # Internal pipeline
    # ------------------------------------------------------------------

    def _execute_pipeline(
        self,
        purpose: str,
        odi_weights: str,
        resume_state: dict | None = None,
    ) -> ABSUBESTResult:
        """Execute the ABSUBEST pipeline stages."""
        from absubest.skills.s1_odi_precheck import odi_precheck
        from absubest.skills.s2_moral_screen import run_moral_screens
        from absubest.skills.s3_purpose import PurposeCrystallizer
        from absubest.skills.s4_constraint import ConstraintClassifier
        from absubest.skills.s5_dimension import DimensionDeriver
        from absubest.skills.s6_coverage import CoverageGenerator
        from absubest.skills.s7_evaluate import Evaluator
        from absubest.skills.s8_certify import Certifier
        from absubest.skills.s9_transcend import Transcender
        from absubest.skills.s10_verify import Verifier
        from absubest.skills.s11_portfolio import PortfolioAssembler
        from absubest.skills.s12_declare import DeclarationDrafter
        from absubest.skills.s13_bias import BiasSteward
        from absubest.skills.s15_registry import ABSUBESTRegistry

        # ---- 1. EXISTENTIAL-RISK CHECK (P10.1 / P0b) ----
        is_existential = self._check_existential_risk(purpose)
        if is_existential:
            return self._existential_risk_response(purpose)

        # ---- 2. MORAL SCREENS (P6 + P6b) ----
        moral = run_moral_screens(purpose)
        if moral.get("P6") == "FAIL":
            return self._hard_refusal(purpose, "P6 consequentialist moral screen failed")
        if moral.get("P6b") == "FAIL":
            return self._hard_refusal(purpose, "P6b deontological moral screen failed")

        # ---- 3. ODI PRE-CHECK (P1) ----
        precheck = odi_precheck(purpose, {})
        coverage_class = precheck.get("coverage_class", "heuristic")
        routing = precheck.get("routing", "full")

        # ---- 4. ODI COMPUTATION ----
        odi = self._compute_odi(precheck, odi_weights)

        # ---- 5. BLUEPRINT GENERATION ----
        blueprint = self._generate_blueprint(odi, coverage_class)

        # ---- 6. STAGE A — PURPOSE CRYSTALLIZATION ----
        pc = PurposeCrystallizer()
        u_spec = pc.crystallize(purpose)
        coherence = pc.verify_coherence(u_spec)

        # ---- 7. STAGE B — CONSTRAINT ONTOLOGY ----
        cc = ConstraintClassifier()
        constraints = cc.classify({"purpose": purpose})

        # ---- 8. STAGE C — DIMENSION DERIVATION ----
        dd = DimensionDeriver()
        dimensions = dd.derive(u_spec)
        bias_disclosure = dd.disclose_biases()

        # ---- 9. STAGE D — SOLUTION-SPACE CONSTRUCTION ----
        cg = CoverageGenerator()
        candidates = cg.generate(purpose, u_spec, dimensions)
        coverage_report = cg.coverage_report()

        # ---- 10. STAGE E — FULL-SPECTRUM EVALUATION ----
        ev = Evaluator()
        scores = ev.evaluate(candidates, dimensions)

        # ---- 11. STAGE F — OPTIMALITY CERTIFICATION ----
        cert = Certifier()
        certificate = cert.certify(scores, odi)
        residual_risk = cert.residual_risk_label()

        # ---- 12. COUNTER-OPTIMIZATION (Layer 2; ODI ≥ 7) ----
        counter_opt_result = None
        p11_tier = None
        if odi >= 7.0:
            pa = PortfolioAssembler()
            portfolio = pa.assemble(purpose, scores.get("best"))
            diversity = pa.diversity_score(portfolio)
            if diversity < 0.3:
                return self._hard_refusal(
                    purpose,
                    f"Portfolio diversity D(Π)={diversity:.2f} < 0.3 (P11 Tier 3)",
                )
            p11_tier = "Tier 1" if diversity >= 0.5 else "Tier 2"
            concessions = pa.run(portfolio)
            counter_opt_result = {"diversity": diversity, "concessions": concessions}

        # ---- 13. STAGE G — TRANSCENDENCE ----
        tr = Transcender()
        if certificate.get("gap_detected", False):
            improved = tr.transcend(purpose, u_spec, scores, certificate)
            if improved:
                # Re-evaluate with improved solution
                scores = ev.evaluate(improved, dimensions)
                certificate = cert.certify(scores, odi)

        # ---- 14. STAGE H — VERIFICATION & IMMORTALIZATION ----
        ver = Verifier()
        verification = ver.verify(scores, certificate)

        # ---- BIAS STEWARD ----
        bias_report = None
        if self.config.bias_steward_enabled:
            bs = BiasSteward()
            bias_report = bs.audit(task_id=self.config.task_id, scores=scores)

        # ---- DECLARATION DRAFTING ----
        ddraft = DeclarationDrafter()
        declaration_text = ddraft.draft(
            purpose=purpose,
            u_spec=u_spec,
            scores=scores,
            certificate=certificate,
            moral_screens=moral,
            odi=odi,
            precheck=precheck,
            bias_report=bias_report,
            counter_opt=counter_opt_result,
            config=self.config,
        )

        # ---- COMPARABILITY HEADER (P13) ----
        header = self._build_comparability_header(purpose, u_spec, scores.get("best", 0))

        # Build result
        result = ABSUBESTResult(
            purpose=purpose,
            solution=certificate.get("best_solution", ""),
            utility=scores.get("best", 0.0),
            certificate=certificate.get("type", "portfolio-concession"),
            certificate_method=certificate.get("method", "heuristic"),
            residual_risk=residual_risk,
            declaration=declaration_text,
            moral_screens=moral,
            odi_score=odi,
            comparability_header=header,
            expiration_date=self._expiration_date(),
            reverification_triggers=self._default_triggers(),
            p11_tier=p11_tier,
            bias_audit=bias_report,
            solution_text=str(certificate.get("best_solution", "")),
            task_id=self.config.task_id,
        )

        # ---- ARCHIVE ----
        try:
            registry = ABSUBESTRegistry()
            registry.archive(result)
        except Exception:
            pass  # non-fatal in Phase 1

        # ---- STATE PERSISTENCE ----
        if self.config.state_persistence:
            from absubest.skills.s14_state import StatePersistence

            sp = StatePersistence()
            sp.checkpoint(self.config.task_id, {"result": result})

        return result

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _check_existential_risk(self, purpose: str) -> bool:
        """Check if purpose is classified existential-risk (P0b)."""
        risk_keywords = [
            "superintelligence",
            "human extinction",
            "civilizational collapse",
            "unaligned AGI",
            "existential risk",
            "weaponized AGI",
        ]
        pl = purpose.lower()
        return any(kw in pl for kw in risk_keywords)

    def _existential_risk_response(self, purpose: str) -> ABSUBESTResult:
        return ABSUBESTResult(
            purpose=purpose,
            solution=None,
            utility=0.0,
            certificate="N/A",
            certificate_method="N/A",
            residual_risk="existential-risk task — requires external review board sign-off",
            declaration="HARD REFUSAL: Purpose classified as existential-risk (P0b). "
                        "External review board sign-off is required before any optimization.",
            moral_screens={"P6": "PASS", "P6b": "PASS", "P0b": "TRIGGERED"},
            odi_score=10.0,
            comparability_header={},
            expiration_date=self._expiration_date(),
            reverification_triggers=[],
            p11_tier=None,
            bias_audit=None,
            task_id=self.config.task_id,
        )

    def _hard_refusal(self, purpose: str, reason: str) -> ABSUBESTResult:
        return ABSUBESTResult(
            purpose=purpose,
            solution=None,
            utility=0.0,
            certificate="HARD REFUSAL",
            certificate_method="N/A",
            residual_risk="refused",
            declaration=f"HARD REFUSAL: {reason}",
            moral_screens={"P6": "PASS", "P6b": "PASS"},
            odi_score=0.0,
            comparability_header={},
            expiration_date=self._expiration_date(),
            reverification_triggers=[],
            p11_tier=None,
            bias_audit=None,
            task_id=self.config.task_id,
        )

    def _compute_odi(self, precheck: dict, weights: str) -> float:
        """Compute Optimality Demand Index."""
        harm = 1 if precheck.get("harm_check", False) else 0
        scale = 1 if precheck.get("scale_check", False) else 0
        irreversible = 1 if not precheck.get("reversible_check", True) else 0

        w_I = 5 if irreversible else 1
        w_B = 2 if scale else 1
        w_M = 2 if harm else 1
        w_C = 0.5

        raw = (w_I + w_B + w_M + w_C) / (w_I + w_B + w_M + w_C) * 10  # placeholder
        odi = min(10.0, max(0.0, raw * 0.7 + 0.5))
        return odi

    def _generate_blueprint(self, odi: float, coverage_class: str) -> dict:
        """Generate task blueprint from ODI and coverage class."""
        if odi < 4:
            pipeline = "lite"
        elif odi < 7:
            pipeline = "express"
        else:
            pipeline = "full"
        return {
            "odi": odi,
            "pipeline": pipeline,
            "coverage_class": coverage_class,
            "tier": 1 if odi < 4 else (2 if odi < 7 else 4),
        }

    def _build_comparability_header(
        self, purpose: str, u_spec: dict, utility: float
    ) -> dict[str, str]:
        return {
            "framework_id": f"ABSUBEST v3.1 (Deployment #2)",
            "purpose_hash": hashlib.sha256(purpose.encode()).hexdigest()[:16],
            "utility_spec_hash": hashlib.sha256(
                json.dumps(u_spec, sort_keys=True).encode()
            ).hexdigest()[:16],
            "context_hash": hashlib.sha256(
                json.dumps(self.config.__dict__, sort_keys=True).encode()
            ).hexdigest()[:16],
            "U(x*)": f"{utility:.4f}",
            "expiration": self._expiration_date(),
        }

    def _expiration_date(self) -> str:
        from datetime import timedelta
        return (datetime.now(timezone.utc) + timedelta(days=180)).strftime("%Y-%m-%d")

    @staticmethod
    def _default_triggers() -> list[str]:
        return [
            "external deployment",
            "benchmark suite construction",
            "framework update",
            "expiration",
        ]
