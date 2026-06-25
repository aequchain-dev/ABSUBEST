---
skill_id: S5
name: Dimension Derivation + Bias Disclosure
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C3 + C.bias + Patch P5
---
TRIGGER CONDITIONS:
  - After S4 (Stage B) completes; before Stage D
  - ODI ≥ 7 triggers mandatory Bias Correction Budget

INPUTS:
  - utility U, solution space X̃
  - value ontology (default: ABSUBEST-Default v3.1)
  - bias inventory (8 biases from v3.1 Part 7)

PROCEDURE:
  1. Concept algebra: decompose U into constituent value predicates → dimension candidates
  2. Causal influence tracing: for each component of P, trace measurable properties → dimension candidates
  3. Value-ontology mapping: cross-reference against comprehensive ontology
  4. Deduplication & orthogonalization
  5. Weighting (elicited or derived)
  6. Completeness certificate
  7. C.bias Bias Disclosure (mandatory):
     a. Ontology declaration (name, version, tradition)
     b. Bias acknowledgment (8 checkboxes + Other)
     c. Bias Correction Budget (mandatory if ODI ≥ 7):
        - Perspective Panel ($/hrs)
        - Co-Design Sessions ($/hrs)
        - Tradition Consultation ($/hrs)
        - Red-Team for Bias ($/hrs)
        - TOTAL must be > $0 for ODI ≥ 7
     d. Mitigation actions taken (documented list)

OUTPUTS:
  - Dimension set D = {d_1, ..., d_k}
  - Aggregate metric M(x) = Σ w_i · d_i(x)
  - Completeness certificate
  - Bias Disclosure record
  - Bias Correction Budget (or "insufficient" flag)

CERTIFICATION HOOKS:
  - D and M specification hashed into P13 comparability header
  - Bias Disclosure archived in declaration
  - If budget insufficient: declaration MUST state "Bias correction not resourced; residual distortion likely on [dimensions]"

FAILURE MODES:
  - F4 Dimensional blindness → mitigated by completeness certificate + blind-spot oracle
  - F18 Bias disclosure as absolution → mitigated by mandatory budget for ODI ≥ 7

INTEGRATION:
  - Invoked by: Stage-Executor-C sub-agent (with Bias-Steward oversight)
  - Operationalized by: T5 (dimension_derive.py), T13 (bias_steward.py), MCP-2, MCP-6
  - Outputs feed: Stage D (solution-space construction on X̃, D)
