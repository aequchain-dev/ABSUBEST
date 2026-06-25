---
skill_id: S15
name: Cross-Framework Comparability Registry
version: 0.1
lineage: ABSUBEST v3.1 — Patch P13
---
TRIGGER CONDITIONS:
  - After S12 (declaration drafting) completes
  - On registry query from external framework

INPUTS:
  - declaration with P13 comparability header
  - registry (SQLite database of all declarations)

PROCEDURE:
  1. Extract comparability header (framework_id, purpose_hash, utility_spec_hash, context_hash, solution_hash, U(x*), U_max, certification_level, residual_risk)
  2. Insert into registry
  3. Comparison rules:
     a. Same purpose_hash + same utility_spec_hash → compare directly on U(x*)
     b. Same purpose_hash + different utility_spec_hash → harmonize (find common U_common); re-evaluate both; compare on U_common; note harmonization gap
     c. Different purpose_hash → not comparable
  4. Dominance check: query "does any declaration dominate declaration D on U_common?"
  5. Re-verification scheduling: when trigger fires, mark declaration as "re-verification pending"

OUTPUTS:
  - Registry entry
  - Comparison report (if queried)
  - Dominance alert (if dominated)
  - Re-verification schedule

CERTIFICATION HOOKS:
  - Registry is the authoritative source for declaration validity
  - Dominated declarations flagged for re-verification

FAILURE MODES:
  - F23 Declarations not interoperable → mitigated by P13 protocol
  - F31 Cross-agent declaration inconsistency → mitigated by registry consistency enforcement

INTEGRATION:
  - Invoked by: Declaration-Archivist sub-agent
  - Operationalized by: T15 (registry.py), Pgrm-4 (absubest-archive), MCP-4
  - Outputs feed: practitioner (for dominance alerts); orchestrator (for re-verification triggers)
