---
skill_id: S11
name: Counter-Optimizer Portfolio Assembly
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C7 + Patches P4 + P11
---
TRIGGER CONDITIONS:
  - ODI ≥ 4 (recommended) or ODI ≥ 7 (mandatory)
  - During S10 verification

INPUTS:
  - purpose P, x*, context C
  - paradigm tags inventory (LLM-p, LLM-ft, symbolic, evolutionary, bayesian, RL, human-expert, human-naive, random, hybrid)
  - paradigm diversity matrix (P4)

PROCEDURE:
  1. Select portfolio members per ODI:
     - ODI 4–5: 1 paradigm-diverse member, D(Π) ≥ 0.40
     - ODI 6–7: ≥2 members, D(Π) ≥ 0.55
     - ODI 8–10: ≥3 members + random injection, D(Π) ≥ 0.65
     - Existential-risk: ≥5 members + human panel, D(Π) ≥ 0.70
  2. Allocate budgets: 50% strongest / 30% diverse / 20% distributed
  3. Each member: produce x' with U(x') > U(x*), OR formally concede
  4. Aggregate concessions:
     - If any member produces improvement → incorporate, re-certify, re-counter-opt
     - If all concede → portfolio soundness established (Theorem 3')
     - If some inconclusive → declaration downgraded
  5. P11 fallback tiers:
     - Tier 1 (0.5–threshold): proceed, cap guarantee at "statistical"
     - Tier 2 (0.3–0.5): proceed only if primary is FORMAL, cap at "statistical"
     - Tier 3 (<0.3): REFUSE declaration
  6. Game-theoretic caveat: if members can model each other, strategic concession possible; mitigated by diversity + random injection + trace audit

OUTPUTS:
  - Counter-Optimizer Portfolio Report:
    - Members with paradigm tags
    - Budget consumption per member
    - Concession log per member (with search traces)
    - Diversity score D(Π) with threshold
    - P11 tier (if fallback applied)
    - Aggregate outcome
    - Game-theoretic caveat acknowledgment

CERTIFICATION HOOKS:
  - Portfolio report archived in declaration
  - Suspicious concessions flagged (budget < 80% consumed + "exhausted_budget" reason)

FAILURE MODES:
  - F8 Counter-opt collusion → mitigated by P4 diversity + random injection
  - F12 Strategic counter-opt concession → mitigated by trace audit + random member injection
  - F16 Portfolio theater → mitigated by P4 machine-checkable metric
  - F21 No protocol when diversity < threshold → mitigated by P11 fallback tiers

INTEGRATION:
  - Invoked by: Counter-Opt-Manager sub-agent
  - Operationalized by: T11 (portfolio_assemble.py), Pgrm-3 (absubest-counter-opt), MCP-3
  - Outputs feed: S10 (verification) and S8 (certification)
