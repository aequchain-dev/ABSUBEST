"""
ABSUBEST MCP-2 Stage-Executor Server — FastMCP implementation.

Exposes all 8 pipeline stages (A–H) as individual callable tools
for granular agent orchestration. Each tool delegates to the
corresponding ABSUBEST skill module.

Tools:
    ping                → {"pong": true, "server": "absubest-stage"}
    stage_a_crystallize → Run Stage A (Purpose Crystallization)
    stage_b_ontology    → Run Stage B (Constraint Ontology)
    stage_c_dimensions  → Run Stage C (Dimension Derivation + Bias)
    stage_d_coverage    → Run Stage D (Solution-Space Construction)
    stage_e_evaluate    → Run Stage E (Full-Spectrum Evaluation)
    stage_f_certify     → Run Stage F (Optimality Certification)
    stage_g_transcend   → Run Stage G (Transcendence)
    stage_h_verify      → Run Stage H (Verification & Immortalization)
    run_full_pipeline   → Run all 8 stages in sequence
"""

from __future__ import annotations

import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

from absubest.core.orchestrator import ABSUBESTResult

# Skill imports
from absubest.skills.s3_purpose import PurposeCrystallizer
from absubest.skills.s4_constraint import ConstraintClassifier
from absubest.skills.s5_dimension import DimensionDeriver
from absubest.skills.s6_coverage import CoverageGenerator
from absubest.skills.s7_evaluate import Evaluator
from absubest.skills.s8_certify import Certifier
from absubest.skills.s9_transcend import Transcender
from absubest.skills.s10_verify import Verifier

logger = logging.getLogger("absubest.mcp.stage")

# ── Server ──────────────────────────────────────────────────────────────────

mcp = FastMCP(
    "absubest-stage",
    instructions="ABSUBEST MCP-2 Stage-Executor Server",
)

# ── Meta ────────────────────────────────────────────────────────────────────


@mcp.tool()
def ping() -> dict:
    """returns {"pong": true, "server": "absubest-stage"}"""
    return {"pong": True, "server": "absubest-stage"}


# ── Stage A: Purpose Crystallization ──────────────────────────────────────


@mcp.tool()
def stage_a_crystallize(purpose: str) -> dict:
    """Run Stage A: convert purpose into operational utility function.

    Args:
        purpose: the purpose statement
    """
    if not purpose:
        raise ValueError("Missing/invalid 'purpose' (required string)")

    crystallizer = PurposeCrystallizer()
    u_spec = crystallizer.crystallize(purpose)
    coherence = crystallizer.verify_coherence(u_spec)

    return {
        "stage": "A",
        "purpose": purpose,
        "u_spec": u_spec,
        "coherence": coherence,
    }


# ── Stage B: Constraint Ontology ──────────────────────────────────────────


@mcp.tool()
def stage_b_ontology(purpose: str, explicit_constraints: list[str] | None = None) -> dict:
    """Run Stage B: classify constraints and apply liberation protocol.

    Args:
        purpose: the purpose statement
        explicit_constraints: explicit constraint list
    """
    if not purpose:
        raise ValueError("Missing/invalid 'purpose' (required string)")

    classifier = ConstraintClassifier()
    constraints = classifier.classify({
        "purpose": purpose,
        "explicit_constraints": explicit_constraints or [],
    })
    liberation = classifier.liberation_protocol()

    return {
        "stage": "B",
        "purpose": purpose,
        "constraints": constraints,
        "liberation": liberation,
        "n_constraints": len(constraints),
    }


# ── Stage C: Dimension Derivation + Bias ──────────────────────────────────


@mcp.tool()
def stage_c_dimensions(u_spec: dict) -> dict:
    """Run Stage C: derive evaluation dimensions and disclose biases.

    Args:
        u_spec: utility specification from Stage A
    """
    if not u_spec:
        raise ValueError("Missing/invalid 'u_spec' (required dict)")

    deriver = DimensionDeriver()
    dimensions = deriver.derive(u_spec)
    biases = deriver.disclose_biases()
    budget = deriver.get_bias_correction_budget()

    return {
        "stage": "C",
        "dimensions": dimensions,
        "n_dimensions": len(dimensions),
        "bias_disclosures": biases,
        "correction_budget": budget,
    }


# ── Stage D: Solution-Space Construction ──────────────────────────────────


@mcp.tool()
def stage_d_coverage(
    purpose: str,
    u_spec: dict,
    dimensions: list[dict],
    n_candidates: int = 5,
) -> dict:
    """Run Stage D: generate candidate solutions with coverage report.

    Args:
        purpose: the purpose statement
        u_spec: utility specification
        dimensions: derived dimensions
        n_candidates: number of candidates (default 5)
    """
    if not purpose:
        raise ValueError("Missing/invalid 'purpose' (required string)")

    if not u_spec:
        raise ValueError("Missing/invalid 'u_spec' (required dict)")

    if not dimensions:
        raise ValueError("Missing/invalid 'dimensions' (required list)")

    if not isinstance(n_candidates, int) or n_candidates < 1:
        n_candidates = 5

    generator = CoverageGenerator()
    candidates = generator.generate(purpose, u_spec, dimensions, n_candidates)
    report = generator.coverage_report()

    return {
        "stage": "D",
        "candidates": candidates,
        "n_candidates": len(candidates),
        "coverage_report": report,
    }


# ── Stage E: Full-Spectrum Evaluation ─────────────────────────────────────


@mcp.tool()
def stage_e_evaluate(
    candidates: list[dict],
    dimensions: list[dict],
    methods: list[str] | None = None,
) -> dict:
    """Run Stage E: evaluate candidates across all dimensions.

    Args:
        candidates: candidates from Stage D
        dimensions: dimensions from Stage C
        methods: evaluation methods to use
    """
    if not candidates:
        raise ValueError("Missing/invalid 'candidates' (required list)")

    if not dimensions:
        raise ValueError("Missing/invalid 'dimensions' (required list)")

    evaluator = Evaluator()
    results = evaluator.evaluate(candidates, dimensions, methods or None)

    return {
        "stage": "E",
        "results": results,
        "n_candidates": len(candidates),
        "methods_used": methods or evaluator.EVALUATION_METHODS,
    }


# ── Stage F: Optimality Certification ─────────────────────────────────────


@mcp.tool()
def stage_f_certify(evaluation: dict, odi: float = 5.0, epsilon: float = 0.01) -> dict:
    """Run Stage F: produce optimality certificate.

    Args:
        evaluation: evaluation results from Stage E
        odi: ODI score (default 5.0)
        epsilon: optimality gap (default 0.01)
    """
    if not evaluation:
        raise ValueError("Missing/invalid 'evaluation' (required dict)")

    certifier = Certifier()
    certificate = certifier.certify(evaluation, odi, epsilon)
    residual_risk = certifier.residual_risk_label()

    return {
        "stage": "F",
        "certificate": certificate,
        "residual_risk": residual_risk,
    }


# ── Stage G: Transcendence ────────────────────────────────────────────────


@mcp.tool()
def stage_g_transcend(purpose: str, u_spec: dict, evaluation: dict, certificate: dict) -> dict:
    """Run Stage G: apply transcendence operators to close gaps.

    Args:
        purpose: original purpose
        u_spec: utility specification
        evaluation: evaluation results
        certificate: certification result
    """
    if not purpose:
        raise ValueError("Missing/invalid 'purpose' (required string)")

    if not all([u_spec, evaluation, certificate]):
        raise ValueError("Missing required params: u_spec, evaluation, certificate")

    transcender = Transcender()
    improved = transcender.transcend(purpose, u_spec, evaluation, certificate)

    return {
        "stage": "G",
        "gap_analysis": transcender._gaps if hasattr(transcender, "_gaps") else [],
        "improved_candidates": improved,
        "has_improvement": improved is not None and len(improved) > 0,
    }


# ── Stage H: Verification & Immortalization ───────────────────────────────


@mcp.tool()
def stage_h_verify(evaluation: dict, certificate: dict, purpose: str = "") -> dict:
    """Run Stage H: verify result and produce declaration draft.

    Args:
        evaluation: evaluation results
        certificate: certification result
        purpose: purpose for declaration text
    """
    if not all([evaluation, certificate]):
        raise ValueError("Missing required params: evaluation, certificate")

    verifier = Verifier()
    verification = verifier.verify(evaluation, certificate)

    return {
        "stage": "H",
        "verification": verification,
        "verdict": verification.get("verdict", "unknown"),
    }


# ── Full Pipeline Run ─────────────────────────────────────────────────────


@mcp.tool()
def run_full_pipeline(
    purpose: str,
    explicit_constraints: list[str] | None = None,
    n_candidates: int = 5,
    odi: float = 5.0,
    epsilon: float = 0.01,
) -> dict:
    """Run all 8 stages in sequence.

    Args:
        purpose: the purpose statement
        explicit_constraints: constraint list
        n_candidates: number of candidates (default 5)
        odi: ODI score (default 5.0)
        epsilon: optimality gap (default 0.01)
    """
    if not purpose:
        raise ValueError("Missing/invalid 'purpose' (required string)")

    pipeline_log: list[dict] = []

    # Stage A
    crystallizer = PurposeCrystallizer()
    u_spec = crystallizer.crystallize(purpose)
    coherence = crystallizer.verify_coherence(u_spec)
    pipeline_log.append({"stage": "A", "status": "completed"})

    # Stage B
    classifier = ConstraintClassifier()
    constraints = classifier.classify({
        "purpose": purpose,
        "explicit_constraints": explicit_constraints or [],
    })
    liberation = classifier.liberation_protocol()
    pipeline_log.append({"stage": "B", "status": "completed", "n_constraints": len(constraints)})

    # Stage C
    deriver = DimensionDeriver()
    dimensions = deriver.derive(u_spec)
    biases = deriver.disclose_biases()
    budget = deriver.get_bias_correction_budget()
    pipeline_log.append({"stage": "C", "status": "completed", "n_dimensions": len(dimensions)})

    # Stage D
    generator = CoverageGenerator()
    candidates = generator.generate(purpose, u_spec, dimensions, n_candidates)
    coverage_report = generator.coverage_report()
    pipeline_log.append({"stage": "D", "status": "completed", "n_candidates": len(candidates)})

    # Stage E
    evaluator = Evaluator()
    evaluation = evaluator.evaluate(candidates, dimensions)
    pipeline_log.append({"stage": "E", "status": "completed"})

    # Stage F
    certifier = Certifier()
    certificate = certifier.certify(evaluation, odi, epsilon)
    residual_risk = certifier.residual_risk_label()
    pipeline_log.append({"stage": "F", "status": "completed", "method": certificate.get("method")})

    # Stage G (if gap detected)
    gap_detected = certificate.get("gap_detected", False)
    improved = None
    if gap_detected:
        transcender = Transcender()
        improved = transcender.transcend(purpose, u_spec, evaluation, certificate)
        pipeline_log.append({
            "stage": "G",
            "status": "completed" if improved else "no_improvement",
        })

    # Stage H
    verifier = Verifier()
    verification = verifier.verify(evaluation, certificate)

    # Build result summary
    best_id = evaluation.get("best_id", "")
    best_utility = evaluation.get("best", 0.0)

    pipeline_log.append({"stage": "H", "status": "completed", "verdict": verification.get("verdict")})

    return {
        "purpose": purpose,
        "pipeline_log": pipeline_log,
        "n_stages_completed": len(pipeline_log),
        "result": {
            "best_solution_id": best_id,
            "best_utility": best_utility,
            "certificate_method": certificate.get("method"),
            "gap_detected": gap_detected,
            "verification_verdict": verification.get("verdict"),
            "residual_risk": residual_risk,
        },
        "summary": {
            "u_spec": u_spec,
            "constraints": len(constraints),
            "dimensions": len(dimensions),
            "candidates": len(candidates),
            "certificate": certificate,
            "verification": verification,
        },
    }


# ── main ────────────────────────────────────────────────────────────────────


def main() -> None:
    """Entry point for `absubest-stage-mcp` — run FastMCP over stdio."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
