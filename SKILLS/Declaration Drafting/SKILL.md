---
skill_id: S12
name: Declaration Drafting
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C9 (declaration) + Patches P7 + P13
---
TRIGGER CONDITIONS:
  - After S10 (verification) completes

INPUTS:
  - x* with certificate
  - full process trace
  - counter-opt report
  - verification report
  - bias disclosure
  - context C, knowledge horizon K

PROCEDURE:
  1. Compose Comparability Header (P13):
     - framework_id, purpose_hash (SHA-256), utility_spec_hash, context_hash, solution_hash
     - U(x*), U_max, certification_level, residual_risk
  2. Compose Epistemic Declaration:
     - Purpose P (formal), Context C, Moral Screens (P6/P6b/P0b)
     - ODI (with weight justification)
     - Pre-Check record, Coverage class, Tier
     - Solution x*, U(x*)
     - Certification (method, certificate ref, residual risk)
     - Counter-optimization (portfolio, diversity, outcome, caveat)
     - Verification methods (with strengths; guarantee = weakest)
     - Bias Disclosure (ontology, 8 checks, budget, self-app bias)
     - Knowledge horizon K
     - Limitations (immutable / design / bias correction)
     - Empirical status (deployments count)
     - Expiration date
     - Re-verification triggers
     - Indexical scope
  3. Compose Ceremonial Absolute Best Declaration:
     - Regulative ideal invocation (Stratum III)
     - Orientation, not attainment
  4. P7 Uncertainty Sign-off (if ODI ≥ 7 AND single-trajectory):
     - Mandatory accountable-authority signature
  5. Archive to declaration registry (P13)

OUTPUTS:
  - Two-tier declaration document
  - Comparability header (P13)
  - P7 sign-off block (if applicable)
  - Archive entry with full trace

CERTIFICATION HOOKS:
  - Declaration archived with P13 header for cross-framework registry lookup
  - P7 sign-off mandatory for ODI ≥ 7 single-trajectory (declaration invalid without)

FAILURE MODES:
  - F17 Convergence theater → mitigated by P7 sign-off + guarantee cap
  - Declaration overclaiming → mitigated by two-tier separation (Epistemic vs Ceremonial)

INTEGRATION:
  - Invoked by: Stage-Executor-H sub-agent (with Declaration-Archivist oversight)
  - Operationalized by: T12 (declare.py), Pgrm-4 (absubest-archive), MCP-2, MCP-4
  - Outputs feed: archive, practitioner, P13 registry
