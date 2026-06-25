"""
ABSUBEST — Absolute Best Framework
====================================
Meta-optimizer framework: given any explicit purpose, dynamically synthesizes
and executes the optimal optimization process for that purpose.

Version: 0.1 (Deployment #2 — Phase 1 build)
Lineage: ABSUBEST v3.1 → Deployment #2
License: MIT or Apache 2.0

See SUITE/AGENT.md for the orchestrator spec, SUITE/SKILLS.md for skill specs,
and SUITE/TOOLING.md for tooling specs.
"""

from __future__ import annotations

__version__ = "0.1.0"
__absubest_version__ = "3.1"

from .core.orchestrator import ABSUBEST
from .cli import main as cli_main
from .schema import SCHEMAS, validate, validate_json, validate_type, list_schemas

__all__ = [
    "ABSUBEST",
    "cli_main",
    "SCHEMAS",
    "validate",
    "validate_json",
    "validate_type",
    "list_schemas",
]
