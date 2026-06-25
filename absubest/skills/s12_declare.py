"""
S12 — Declaration Drafting
============================
Two-tier declaration: Epistemic (technical) + Ceremonial (human-readable).
P7 Uncertainty Sign-off for ODI ≥ 7 single-trajectory.
P13 comparability header with SHA-256 hashes.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone, timedelta
from typing import Any

from absubest.core.orchestrator import ABSUBESTConfig


class DeclarationDrafter:
    """Two-tier declaration drafting (S12/T12)."""

    def draft(
        self,
        purpose: str,
        u_spec: dict,
        scores: dict,
        certificate: dict,
        moral_screens: dict,
        odi: float,
        precheck: dict,
        bias_report: list[dict] | None = None,
        counter_opt: dict | None = None,
        config: ABSUBESTConfig | None = None,
    ) -> str:
        """Draft a complete two-tier declaration.

        Tier 1 — Epistemic Declaration (technical, machine-readable facts)
        Tier 2 — Ceremonial Declaration (human-readable, signed by framework)

        Returns:
            Full declaration text
        """
        tier1 = self._tier1_epistemic(
            purpose, u_spec, scores, certificate,
            moral_screens, odi, precheck, bias_report, counter_opt,
        )
        tier2 = self._tier2_ceremonial(
            purpose, odi, scores, certificate, config,
        )
        return f"{tier1}\n\n---\n\n{tier2}"

    def _tier1_epistemic(
        self,
        purpose: str,
        u_spec: dict,
        scores: dict,
        certificate: dict,
        moral_screens: dict,
        odi: float,
        precheck: dict,
        bias_report: list[dict] | None,
        counter_opt: dict | None,
    ) -> str:
        """Tier 1: Technical, machine-readable epistemic declaration."""
        lines = [
            "=" * 60,
            "TIER 1 — EPISTEMIC DECLARATION",
            "=" * 60,
            "",
            f"Framework:        ABSUBEST v3.1 (Deployment #2)",
            f"Date:             {datetime.now(timezone.utc).isoformat()}",
            f"Purpose:          {purpose}",
            f"ODI:              {odi:.2f}",
            f"Cert Method:      {certificate.get('method', 'N/A')}",
            f"U(x*):            {scores.get('best', 0.0):.4f}",
            f"Residual Risk:    {certificate.get('residual_risk_label', 'N/A')}",
            f"Gap Detected:     {certificate.get('gap_detected', False)}",
            "",
            "Moral Screens:",
        ]
        for k, v in moral_screens.items():
            lines.append(f"  {k}: {v}")

        if bias_report:
            lines.append("")
            lines.append("Bias Audit:")
            if isinstance(bias_report, list):
                for b in bias_report:
                    name = b.get("bias", "?")
                    sev = b.get("severity", "?")
                    desc = b.get("description", "")[:60]
                    lines.append(f"  {name} [{sev}]: {desc}")
            elif isinstance(bias_report, dict):
                for k, v in bias_report.items():
                    lines.append(f"  {k}: {v}")

        if counter_opt:
            lines.append("")
            lines.append(f"Counter-Opt Diversity D(Π): {counter_opt.get('diversity', 0):.3f}")

        lines.append("")
        lines.append(self._comparability_block(purpose, u_spec, scores.get("best", 0)))
        return "\n".join(lines)

    def _tier2_ceremonial(
        self,
        purpose: str,
        odi: float,
        scores: dict,
        certificate: dict,
        config: ABSUBESTConfig | None,
    ) -> str:
        """Tier 2: Human-readable ceremonial declaration."""
        lines = [
            "=" * 60,
            "TIER 2 — CEREMONIAL DECLARATION",
            "=" * 60,
            "",
            "ABSUBEST v3.1 certifies that the stated purpose",
            f"  \"{purpose}\"",
            f"has been optimized with ODI {odi:.2f} rigor.",
            "",
            f"Best utility: U(x*) = {scores.get('best', 0.0):.4f}",
            f"Certificate:  {certificate.get('method', 'N/A')}",
            "",
        ]
        if certificate.get("gap_detected", False):
            lines.append("⚠  A gap remains — transcendence operator may be required.")
            lines.append("")

        lines.append("This declaration is indexical — bounded by context C,")
        lines.append(f"date {datetime.now(timezone.utc).strftime('%Y-%m-%d')}, and knowledge horizon K.")
        lines.append("")
        lines.append("The Absolute Best remains a regulative ideal (Stratum III, Kantian sense).")
        lines.append("No framework can prove its own optimality from within (Gödel, Tarski).")
        lines.append("")
        lines.append(f"Expiration: {(datetime.now(timezone.utc) + timedelta(days=180)).strftime('%Y-%m-%d')}")
        return "\n".join(lines)

    @staticmethod
    def _comparability_block(purpose: str, u_spec: dict, utility: float) -> str:
        """P13 comparability header with SHA-256 hashes."""
        header = {
            "framework_id": "ABSUBEST v3.1 (Deployment #2)",
            "purpose_hash": hashlib.sha256(purpose.encode()).hexdigest()[:16],
            "utility_spec_hash": hashlib.sha256(
                json.dumps(u_spec, sort_keys=True).encode()
            ).hexdigest()[:16],
            "U(x*)": f"{utility:.4f}",
        }
        return json.dumps({"comparability_header": header}, indent=2)
