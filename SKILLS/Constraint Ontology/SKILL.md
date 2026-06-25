---
skill_id: S4
name: Constraint Ontology
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C2 + B+ Coverage Monotonicity
---
TRIGGER CONDITIONS:
  - After S3 (Stage A) completes; before Stage C

INPUTS:
  - decision space X (initial)
  - constraints (informal list)

PROCEDURE:
  1. Classify each constraint into one of 6 classes:
     - Physical (immutable law of nature)
     - Mathematical (immutable theorem)
     - Resource (hard for current context)
     - Technological (soft; flag for Stage G)
     - Conventional (challenge aggressively)
     - Self-imposed (challenge by default)
  2. Liberation Protocol: for each non-immutable constraint, construct parallel solution space with constraint relaxed; adopt if max U increases
  3. B+ Coverage Monotonicity: when X̃ expands mid-run, re-validate cov(S, X̃') ≥ 1−δ' or launch targeted Stage D'

OUTPUTS:
  - Constraint-augmented solution space X̃
  - Classification table with justifications
  - Liberation outcomes log

CERTIFICATION HOOKS:
  - X̃ specification hashed into P13 comparability header
  - Liberation outcomes archived in declaration

FAILURE MODES:
  - F5 Constraint captivity → mitigated by Liberation Protocol + independent audit
  - Mid-run X̃ expansion invalidating coverage → mitigated by B+ Coverage Monotonicity

INTEGRATION:
  - Invoked by: Stage-Executor-B sub-agent
  - Operationalized by: T4 (constraint_ontology.py), MCP-2
  - Outputs feed: Stage C (dimension derivation on U, X̃)
