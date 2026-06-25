---
skill_id: S10
name: Verification & Immortalization
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C9 (verification)
---
TRIGGER CONDITIONS:
  - After S8 (Stage F) certifies (or S9 transcendence completes)

INPUTS:
  - x* with certificate
  - verification methods available

PROCEDURE:
  1. Multi-method verification:
     a. Adversarial AI red-teaming (find flaws, alternatives, counterexamples)
     b. Blind-spot oracle (model trained on historical failure modes)
     c. Independent re-derivation (separate optimizer/algorithm/team)
     d. Rest-and-re-examine (mandatory delay: hours for micro, weeks for macro)
     e. Counter-optimization (mandatory ODI ≥ 7; see S11)
  2. Honest Method Disclosure: name each method with epistemic strength
  3. Guarantee level = min(strength of all methods used)
  4. Immortalization: archive full trace + certificate + counter-opt report + verification methods + expiration + re-verification triggers

OUTPUTS:
  - Verification report (methods, strengths, guarantee level)
  - Archive entry (full process trace)

CERTIFICATION HOOKS:
  - Verification report archived in declaration
  - Guarantee level capped by weakest method (no overclaiming)

FAILURE MODES:
  - F6 K-horizon overconfidence → mitigated by explicit K + re-verification schedule
  - Verification method bias → mitigated by multi-method requirement

INTEGRATION:
  - Invoked by: Stage-Executor-H sub-agent
  - Operationalized by: T10 (verify.py), MCP-2, MCP-4 (archive)
  - Outputs feed: S12 (declaration drafting)
