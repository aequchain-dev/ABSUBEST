---
skill_id: S7
name: Full-Spectrum Evaluation
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C5 + E+ Time-Consistency Hook
---
TRIGGER CONDITIONS:
  - After S6 (Stage D) completes

INPUTS:
  - candidate set S, dimension set D, aggregate metric M

PROCEDURE:
  1. For each dimension, apply most-precise available method:
     - Simulation (system behavior)
     - Formal verification (correctness, safety, bounds)
     - Expert panel (judgment)
     - Empirical measurement (real-world performance)
     - Causal modeling (counterfactual outcomes)
     - Theoretical analysis (asymptotic/invariant properties)
  2. Cross-scale coherence check (macro / meso / micro)
  3. Identify provisional best x* = argmax_{x∈S} M(x)
  4. E+ Time-Consistency Hook: lightweight re-elicitation on top-3 uncertain tradeoffs; compute drift score d_n; if d_n ≥ 0.05 → pause with 4-option menu

OUTPUTS:
  - Scored candidates {(x, M(x), d_i(x))}
  - Provisional best x* with full dimensional scores
  - Coherence certificate
  - Drift score (with pause-and-ask log if triggered)

CERTIFICATION HOOKS:
  - Scored candidates archived
  - Drift score logged in declaration

FAILURE MODES:
  - Evaluation method bias → mitigated by multi-method requirement
  - F3 Purpose drift → mitigated by E+ Time-Consistency Hook

INTEGRATION:
  - Invoked by: Stage-Executor-E sub-agent
  - Operationalized by: T7 (evaluate.py), Pgrm-2 (absubest-solver), MCP-2
  - Outputs feed: Stage F (optimality certification on x*, S, M, U_max)
