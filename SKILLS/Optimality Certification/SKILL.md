---
skill_id: S8
name: Optimality Certification
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C6 + F+ Honest Residual Risk + Patch P11
---
TRIGGER CONDITIONS:
  - After S7 (Stage E) completes

INPUTS:
  - provisional best x*, candidate set S, metric M, theoretical bound U_max

PROCEDURE:
  1. Attempt escalating certification methods:
     a. Pareto proof (multi-objective; finite Pareto frontier)
     b. Upper-bound attainment (U(x*) = U_max; strongest)
     c. Calibrated statistical bound (ε stated)
     d. Formal proof (Lean/Coq/Z3/Why3; decidable fragments)
     e. Redundant formal (2+ independent proofs; ODI ≥ 9)
     f. Portfolio counter-optimizer concession (uncalibrated; labeled as such)
  2. Honest residual risk labeling (mandatory):
     - Formal proof → residual_risk = "0 (within formal spec)"
     - Calibrated statistical → residual_risk = "quantified: ε=[value]"
     - Portfolio concession → residual_risk = "unquantified: search-complete relative to Π"
     - Mental only → residual_risk = "unquantified: heuristic verification only"
  3. P11 fallback: if portfolio diversity D(Π) < threshold, apply Tier 1/2/3 rules
  4. If certification fails: route to Stage G (transcendence) with gap-source diagnosis

OUTPUTS:
  - Optimality certificate (method, value, residual risk)
  - If failed: gap-source diagnosis (coverage / dimension / constraint / knowledge / formalization)

CERTIFICATION HOOKS:
  - Certificate archived in declaration
  - Residual risk explicitly labeled (no overclaiming)

FAILURE MODES:
  - F1 Premature plateau → mitigated by requiring C2 (formal/stat bound), not just C1
  - F17 Convergence theater → mitigated by P7 sign-off + guarantee cap

INTEGRATION:
  - Invoked by: Stage-Executor-F sub-agent
  - Operationalized by: T8 (certify.py), Pgrm-1 (absubest-prover), MCP-2
  - Outputs feed: Counter-Opt-Manager (S11) and/or Stage G (S9)
