---
skill_id: S3
name: Purpose Crystallization
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C1 + A+.1/A+.2/A+.3
---
TRIGGER CONDITIONS:
  - After Moral Screens pass; first stage of optimization pipeline
  - Re-triggered by Purpose Evolution Protocol (A+.3) when drift detected

INPUTS:
  - purpose P (informal or semi-formal)
  - stakeholder preferences
  - value-ontology declaration (for bias disclosure)

PROCEDURE:
  1. Elicitation interview (automated or human)
  2. Closure test (every stated value either in U, derivable, or excluded)
  3. Tradeoff elicitation (pairwise indifference points)
  4. Utility construction (additive / multi-attribute / non-linear)
  5. Sanity check (U orders test cases per intuition)
  6. A+.1 Coherence Verification (5 axioms: transitivity, independence, continuity, completeness, non-contradiction)
  7. A+.2 Tier 4 Challenge (if Tier 4 candidate): preference elicitation → decomposition → robust satisficing
  8. A+.3 Purpose Evolution hooks (record for re-check at iteration boundaries)
  9. Fast-Track check (P3): if archetype ∈ {AESTHETIC_CREATION, SPIRITUAL_PRACTICE, RELATIONAL_CARE, CULTURAL_CONTINUITY, EMBODIED_KNOWLEDGE}, Tier 4 activates immediately

OUTPUTS:
  - Utility function U: X → ℝ (or Pareto structure / threshold set)
  - Decision space X
  - Success criteria
  - Tier classification (1/2/3/4)
  - Coherence certificate (5 axioms)

CERTIFICATION HOOKS:
  - U specification hashed into P13 comparability header
  - Tier classification archived in declaration

FAILURE MODES:
  - F9 Formalization overreach → mitigated by Tier 4 Challenge Protocol
  - F15 Tier 4 bureaucracy → mitigated by Fast-Track (P3)

INTEGRATION:
  - Invoked by: Stage-Executor-A sub-agent
  - Operationalized by: T3 (purpose_crystallize.py), MCP-2
  - Outputs feed: Stage B (constraint ontology on X)
