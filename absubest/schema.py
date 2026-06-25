"""
ABSUBEST JSON Schema — Formal type definitions for the ABSUBEST protocol.

Defines the canonical schemas for:
  - ABSUBEST Pipeline Request / Response
  - ODI Pre-Check
  - Moral Screen results
  - Blueprint
  - Purpose Crystallization U-spec
  - Constraint Classification
  - Dimension Derivation (with bias disclosure)
  - Coverage Report
  - Full-Spectrum Evaluation
  - Optimality Certificate
  - Counter-Optimizer Portfolio
  - Transcendence Result
  - Verification Result
  - Declaration (Epistemic & Ceremonial)
  - State Persistence checkpoint
  - Registry entry
  - Bias Audit

These schemas serve as the single source of truth for validation across
all Tier 1–4 tooling.

Usage:
    from absubest.schema import SCHEMAS, validate
    errors = validate("declaration", declaration_dict)
"""

from __future__ import annotations

import json
from typing import Any

# ═══════════════════════════════════════════════════════════════════════════
# ODI Pre-Check
# ═══════════════════════════════════════════════════════════════════════════

ODI_PRECHECK_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/odi_precheck.json",
    "title": "ODI Pre-Check",
    "description": "5-question ODI Pre-Check (v3.1 P1). Routes Lite/Express/Full.",
    "type": "object",
    "required": ["purpose", "answers"],
    "properties": {
        "purpose": {"type": "string", "description": "The purpose being evaluated"},
        "answers": {
            "type": "object",
            "minProperties": 5,
            "properties": {
                "q1_value_impact": {"type": "number", "minimum": 0, "maximum": 10},
                "q2_stakeholder_scope": {"type": "number", "minimum": 0, "maximum": 10},
                "q3_irreversibility": {"type": "number", "minimum": 0, "maximum": 10},
                "q4_certainty": {"type": "number", "minimum": 0, "maximum": 10},
                "q5_resource_magnitude": {"type": "number", "minimum": 0, "maximum": 10},
            },
            "additionalProperties": False,
        },
        "odi_score": {"type": "number", "minimum": 0, "maximum": 10},
        "route": {"type": "string", "enum": ["LITE", "EXPRESS", "FULL"]},
        "weight_justifications": {
            "type": "object",
            "additionalProperties": {"type": "string"},
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Moral Screen
# ═══════════════════════════════════════════════════════════════════════════

MORAL_SCREEN_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/moral_screen.json",
    "title": "Moral Screen",
    "description": "P6 consequentialist + P6b deontological + P0b existential-risk screen.",
    "type": "object",
    "required": ["p6_pass", "p6b_pass", "p6_reasoning", "p6b_reasoning"],
    "properties": {
        "p6_pass": {"type": "boolean"},
        "p6b_pass": {"type": "boolean"},
        "p0b_existential_risk": {"type": "boolean"},
        "p6_reasoning": {"type": "string"},
        "p6b_reasoning": {"type": "string"},
        "p0b_reasoning": {"type": "string"},
        "external_review_required": {"type": "boolean"},
        "external_review_obtained": {"type": "boolean"},
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Blueprint (Layer 0)
# ═══════════════════════════════════════════════════════════════════════════

BLUEPRINT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/blueprint.json",
    "title": "Pipeline Blueprint",
    "description": "Layer 0 Meta-Calibrator blueprint defining the pipeline configuration.",
    "type": "object",
    "required": ["odi", "route", "coverage_class", "stages"],
    "properties": {
        "odi": {"type": "number", "minimum": 0, "maximum": 10},
        "route": {"type": "string", "enum": ["LITE", "EXPRESS", "FULL"]},
        "coverage_class": {"type": "string", "enum": ["computable", "heuristic"]},
        "tier": {"type": "integer", "minimum": 1, "maximum": 4},
        "fast_track_eligible": {"type": "boolean"},
        "stages": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["stage", "enabled"],
                "properties": {
                    "stage": {"type": "string"},
                    "enabled": {"type": "boolean"},
                    "rigor": {"type": "string", "enum": ["minimal", "standard", "maximum"]},
                    "resource_allocation": {"type": "number", "minimum": 0, "maximum": 1},
                },
            },
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Purpose Crystallization (U-spec)
# ═══════════════════════════════════════════════════════════════════════════

PURPOSE_U_SPEC_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/purpose_u_spec.json",
    "title": "Purpose Crystallization",
    "description": "Operational utility function U from purpose crystallization (S3).",
    "type": "object",
    "required": ["purpose", "utiity_function", "objective"],
    "properties": {
        "purpose": {"type": "string"},
        "utiity_function": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["linear", "threshold", "multiplicative", "constrained_optimization"]},
                "expression": {"type": "string"},
                "parameters": {"type": "object"},
            },
            "required": ["type", "expression"],
        },
        "objective": {"type": "string", "enum": ["maximize", "minimize", "satisfice", "optimize", "balance"]},
        "tradeoff_weights": {
            "type": "object",
            "additionalProperties": {"type": "number"},
        },
        "coherence": {
            "type": "object",
            "properties": {
                "passed": {"type": "boolean"},
                "axioms_checked": {"type": "array", "items": {"type": "string"}},
                "tier_4_challenge_passed": {"type": "boolean"},
                "evolution_hooks": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Constraint Classification
# ═══════════════════════════════════════════════════════════════════════════

CONSTRAINT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/constraint.json",
    "title": "Constraint Classification",
    "description": "6-class constraint ontology + liberation protocol (S4).",
    "type": "object",
    "required": ["classified", "liberation_protocol"],
    "properties": {
        "classified": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "constraint": {"type": "string"},
                    "class": {
                        "type": "string",
                        "enum": [
                            "physical",
                            "epistemic",
                            "normative",
                            "temporal",
                            "economic",
                            "self_imposed",
                        ],
                    },
                    "testably_redundant": {"type": "boolean"},
                    "justification": {"type": "string"},
                },
                "required": ["constraint", "class"],
            },
        },
        "liberation_protocol": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "constraint": {"type": "string"},
                    "action": {"type": "string"},
                    "expected_benefit": {"type": "string"},
                },
            },
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Dimension Derivation (with Bias Disclosure)
# ═══════════════════════════════════════════════════════════════════════════

DIMENSION_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/dimension.json",
    "title": "Dimension Derivation",
    "description": "Evaluation dimensions derived via concept algebra + causal tracing (S5/C.bias).",
    "type": "object",
    "required": ["dimensions", "methodology"],
    "properties": {
        "dimensions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "justification": {"type": "string"},
                    "scale": {"type": "string"},
                    "weight": {"type": "number", "minimum": 0, "maximum": 1},
                },
                "required": ["name"],
            },
        },
        "methodology": {"type": "string", "enum": ["concept_algebra", "causal_tracing", "hybrid"]},
        "bias_disclosure": {
            "type": "object",
            "properties": {
                "biases_disclosed": {"type": "array", "items": {"type": "string"}},
                "correction_budget": {"type": "number", "minimum": 0},
                "residual_distortion": {"type": "string"},
            },
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Coverage Report
# ═══════════════════════════════════════════════════════════════════════════

COVERAGE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/coverage.json",
    "title": "Coverage Report",
    "description": "Solution-space coverage report (S6, P8 minimal generative coverage).",
    "type": "object",
    "required": ["candidates_count", "coverage_class"],
    "properties": {
        "candidates_count": {"type": "integer", "minimum": 0},
        "coverage_class": {"type": "string", "enum": ["computable", "heuristic"]},
        "coverage_ratio": {"type": "number", "minimum": 0, "maximum": 1},
        "delta_max": {"type": "number", "minimum": 0},
        "heuristic_label": {"type": "string"},
        "sampling_method": {"type": "string"},
        "candidates": {
            "type": "array",
            "items": {"type": "object"},
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Full-Spectrum Evaluation
# ═══════════════════════════════════════════════════════════════════════════

EVALUATION_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/evaluation.json",
    "title": "Full-Spectrum Evaluation",
    "description": "6-method evaluation matrix with cross-scale coherence (S7).",
    "type": "object",
    "required": ["scores", "methods_used"],
    "properties": {
        "scores": {
            "type": "object",
            "additionalProperties:": {
                "type": "object",
                "properties": {
                    "score": {"type": "number", "minimum": 0, "maximum": 10},
                    "methods": {"type": "array", "items": {"type": "string"}},
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                },
            },
        },
        "methods_used": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "simulation",
                    "formal_verification",
                    "expert_panel",
                    "empirical_measurement",
                    "causal_modeling",
                    "theoretical_analysis",
                ],
            },
        },
        "cross_scale_coherence": {"type": "object"},
        "time_consistency_drift": {"type": "number", "minimum": 0},
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Optimality Certificate
# ═══════════════════════════════════════════════════════════════════════════

CERTIFICATE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/certificate.json",
    "title": "Optimality Certificate",
    "description": "Escalating optimality certification with residual risk (S8).",
    "type": "object",
    "required": ["certification_type", "certificate_text"],
    "properties": {
        "certification_type": {
            "type": "string",
            "enum": [
                "pareto_dominance",
                "upper_bound",
                "statistical",
                "formal",
                "redundant_formal",
                "portfolio_concession",
            ],
        },
        "certificate_text": {"type": "string"},
        "residual_risk": {"type": "string"},
        "certified_best": {"type": "string"},
        "certifier": {"type": "string"},
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Counter-Optimizer Portfolio
# ═══════════════════════════════════════════════════════════════════════════

PORTFOLIO_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/portfolio.json",
    "title": "Counter-Optimizer Portfolio",
    "description": "Paradigm-diverse counter-optimizer portfolio (S11, P4).",
    "type": "object",
    "required": ["portfolio", "diversity"],
    "properties": {
        "portfolio": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "paradigm": {"type": "string"},
                    "budget_percent": {"type": "number", "minimum": 0, "maximum": 1},
                    "concessions": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "diversity": {"type": "number", "minimum": 0, "maximum": 1},
        "diversity_threshold_met": {"type": "boolean"},
        "fallback_tier": {"type": "integer", "minimum": 1, "maximum": 3},
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Transcendence Result
# ═══════════════════════════════════════════════════════════════════════════

TRANSCENDENCE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/transcendence.json",
    "title": "Transcendence Result",
    "description": "Result of applying transcendence operators (S9).",
    "type": "object",
    "required": ["operator_applied", "gap_source"],
    "properties": {
        "operator_applied": {
            "type": "string",
            "enum": ["OP_COV", "OP_DIM", "OP_CON", "OP_KNO", "OP_FOR", "OP_SCL"],
        },
        "gap_source": {"type": "string"},
        "improvements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "candidate": {"type": "string"},
                    "delta_before": {"type": "number"},
                    "delta_after": {"type": "number"},
                },
            },
        },
        "re_entry_stage": {"type": "string"},
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Verification Result
# ═══════════════════════════════════════════════════════════════════════════

VERIFICATION_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/verification.json",
    "title": "Verification Result",
    "description": "Multi-method verification output (S10).",
    "type": "object",
    "required": ["methods_used", "overall_verdict"],
    "properties": {
        "methods_used": {
            "type": "array",
            "items": {"type": "string"},
        },
        "overall_verdict": {
            "type": "string",
            "enum": ["verified", "conditionally_verified", "not_verified"],
        },
        "method_results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "method": {"type": "string"},
                    "passed": {"type": "boolean"},
                    "details": {"type": "string"},
                },
            },
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Declaration (Epistemic + Ceremonial)
# ═══════════════════════════════════════════════════════════════════════════

DECLARATION_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/declaration.json",
    "title": "ABSUBEST Declaration",
    "description": "Two-tier declaration: epistemic (formal bounds) + ceremonial (narrative).",
    "type": "object",
    "required": ["purpose", "timestamp", "epistemic", "odai", "registry_id"],
    "properties": {
        "purpose": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "task_id": {"type": "string"},
        "registry_id": {"type": "string"},
        "odai": {
            "type": "object",
            "properties": {
                "odi_score": {"type": "number"},
                "weight_justifications": {"type": "object"},
            },
            "required": ["odi_score"],
        },
        "epistemic": {
            "type": "object",
            "properties": {
                "certification_type": {"type": "string"},
                "residual_risk": {"type": "string"},
                "counter_optimizer_concessions": {"type": "array", "items": {"type": "string"}},
                "diversity_score": {"type": "number"},
                "bias_audit": {"type": "object"},
                "uncertainty_signoff": {"type": "object"},
            },
            "required": ["certification_type", "residual_risk"],
        },
        "ceremonial": {
            "type": "object",
            "properties": {
                "narrative": {"type": "string"},
                "scores_summary": {"type": "object"},
                "next_steps": {"type": "array", "items": {"type": "string"}},
            },
        },
        "p13_comparability_header": {
            "type": "object",
            "properties": {
                "absubest_version": {"type": "string"},
                "framework_hash": {"type": "string"},
                "declaration_hash": {"type": "string"},
                "timestamp": {"type": "string"},
            },
            "required": ["absubest_version", "framework_hash", "declaration_hash"],
        },
        "bias_section": {
            "type": "object",
            "additionalProperties": True,
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# State Persistence Checkpoint
# ═══════════════════════════════════════════════════════════════════════════

STATE_CHECKPOINT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/state_checkpoint.json",
    "title": "State Checkpoint",
    "description": "Checkpoint for P12 state persistence across sessions.",
    "type": "object",
    "required": ["task_id", "checkpoint_time", "stage"],
    "properties": {
        "task_id": {"type": "string"},
        "checkpoint_time": {"type": "string", "format": "date-time"},
        "stage": {"type": "string"},
        "blueprint": {"type": "object"},
        "state": {"type": "object"},
        "metadata": {"type": "object"},
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Registry Entry
# ═══════════════════════════════════════════════════════════════════════════

REGISTRY_ENTRY_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/registry_entry.json",
    "title": "Registry Entry",
    "description": "ABSUBEST declaration registry entry (S15, P13).",
    "type": "object",
    "required": ["id", "timestamp", "purpose", "p13_comparability_header"],
    "properties": {
        "id": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "purpose": {"type": "string"},
        "p13_comparability_header": {
            "type": "object",
            "properties": {
                "absubest_version": {"type": "string"},
                "framework_hash": {"type": "string"},
                "declaration_hash": {"type": "string"},
                "timestamp": {"type": "string"},
            },
            "required": ["absubest_version", "framework_hash", "declaration_hash"],
        },
        "declaration": {"type": "object"},
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Bias Audit
# ═══════════════════════════════════════════════════════════════════════════

BIAS_AUDIT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://absubest.org/schemas/bias_audit.json",
    "title": "Bias Audit",
    "description": "P5/P14 bias detection and correction record (S13).",
    "type": "object",
    "required": ["task_id", "detected_biases"],
    "properties": {
        "task_id": {"type": "string"},
        "detected_biases": {
            "type": "array",
            "items:": {
                "type": "object",
                "properties": {
                    "bias_type": {"type": "string"},
                    "severity": {"type": "number", "minimum": 0, "maximum": 1},
                    "evidence": {"type": "string"},
                    "correction_applied": {"type": "boolean"},
                    "correction": {"type": "string"},
                },
                "required": ["bias_type", "severity", "evidence"],
            },
        },
        "correction_budget_used": {"type": "number"},
        "correction_budget_remaining": {"type": "number"},
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Combined Schema Registry
# ═══════════════════════════════════════════════════════════════════════════

SCHEMAS: dict[str, dict] = {
    "odi_precheck": ODI_PRECHECK_SCHEMA,
    "moral_screen": MORAL_SCREEN_SCHEMA,
    "blueprint": BLUEPRINT_SCHEMA,
    "purpose_u_spec": PURPOSE_U_SPEC_SCHEMA,
    "constraint": CONSTRAINT_SCHEMA,
    "dimension": DIMENSION_SCHEMA,
    "coverage": COVERAGE_SCHEMA,
    "evaluation": EVALUATION_SCHEMA,
    "certificate": CERTIFICATE_SCHEMA,
    "portfolio": PORTFOLIO_SCHEMA,
    "transcendence": TRANSCENDENCE_SCHEMA,
    "verification": VERIFICATION_SCHEMA,
    "declaration": DECLARATION_SCHEMA,
    "state_checkpoint": STATE_CHECKPOINT_SCHEMA,
    "registry_entry": REGISTRY_ENTRY_SCHEMA,
    "bias_audit": BIAS_AUDIT_SCHEMA,
}

# ── Registration ───────────────────────────────────────────────────────────


def register_schema(name: str, schema: dict) -> None:
    """Register an additional schema at runtime."""
    SCHEMAS[name] = schema


def list_schemas() -> dict[str, str]:
    """Return mapping of schema names to their $id values."""
    return {name: schema.get("$id", "") for name, schema in SCHEMAS.items()}


def get_schema(name: str) -> dict | None:
    """Get a schema by name."""
    return SCHEMAS.get(name)


# ── Validation ─────────────────────────────────────────────────────────────

# Simple required-field validation (full JSON Schema validation via `jsonschema` optional)


def validate(schema_name: str, instance: dict) -> list[str]:
    """Validate an instance against a registered schema.

    Returns a list of error strings (empty = valid).
    Uses jsonschema library if available; falls back to required-field check.

    Args:
        schema_name: Name of registered schema.
        instance: Dictionary to validate.

    Returns:
        List of validation error messages. Empty list = valid.
    """
    schema = SCHEMAS.get(schema_name)
    if schema is None:
        return [f"Unknown schema: {schema_name}"]

    # Try jsonschema library first
    try:
        import jsonschema

        validator = jsonschema.Draft202012Validator(schema)
        errors = list(validator.iter_errors(instance))
        if errors:
            return [e.message for e in errors]
        return []
    except ImportError:
        pass

    # Fallback: check required fields only
    errors: list[str] = []
    required = schema.get("required", [])
    for field in required:
        if field not in instance:
            errors.append(f"Missing required field: {field}")
    return errors


def validate_json(schema_name: str, json_str: str) -> list[str]:
    """Validate a JSON string against a schema."""
    try:
        instance = json.loads(json_str)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]
    if not isinstance(instance, dict):
        return ["JSON root must be an object"]
    return validate(schema_name, instance)


def validate_type(
    schema_name: str, instance: Any, raise_on_error: bool = False
) -> bool:
    """Validate and return boolean. Optionally raise on first error."""
    errors = validate(schema_name, instance)
    if errors and raise_on_error:
        raise ValueError(f"Schema '{schema_name}' validation failed: {errors[0]}")
    return len(errors) == 0
