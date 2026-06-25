# SKILLS.md — ABSUBEST-Exactor v0.1
## Skill Library: 15 Skills That Enhance ABSUBEST Framework Application

> **Lineage**: ABSUBEST v3.1 → Deployment #2
> **Format**: ABSUBEST-native (superset of OpenAI/Anthropic skill format — adds certification hooks and failure modes)
> **Status**: best-known characterized alternative; pending external review

Each skill below is a discrete competency that enhances ABSUBEST framework application from an agentic perspective. Skills are invoked by the orchestrator (see `AGENT.md`) and operationalized by tools (see `TOOLING.md`).

---

## Skill Inventory

| Skill | Title | Covers | Patch |
|-------|-------|--------|-------|
| S1 | ODI Pre-Check | C10 (meta-control entry) | P1 |
| S2 | Moral Screen (Consequentialist + Deontological) | P0/P6/P6b | P6, P9 |
| S3 | Purpose Crystallization & Utility Construction | C1, A+.1, A+.2, A+.3 | P3 (Fast-Track) |
| S4 | Constraint Ontology & Liberation | C2, B+ | — |
| S5 | Dimension Derivation + Bias Disclosure | C3, C.bias | P5 |
| S6 | Generative Coverage (Minimal) | C4 | P8 |
| S7 | Full-Spectrum Evaluation | C5, E+ | — |
| S8 | Optimality Certification (Honest Residual Risk) | C6, F+ | P11 fallback |
| S9 | Transcendence Engine | C8 (transcendence) | — |
| S10 | Verification & Immortalization | C9 (verification) | — |
| S11 | Counter-Optimizer Portfolio Assembly | C7, P4, P11 | P4, P11 |
| S12 | Declaration Drafting (Two-Tier + Comparability) | C9 (declaration) | P7, P13 |
| S13 | Bias Steward (P5 + P14) | P5, P14 | P5, P14 |
| S14 | State Persistence (P12) | Macro-task continuity | P12 |
| S15 | Cross-Framework Comparability Registry | P13 | P13 |

---

## Skill Specification Template

```yaml
skill_id: S<N>
name: <skill name>
version: 0.1
lineage: ABSUBEST v3.1 — <patch or core process>

TRIGGER CONDITIONS:
  - <condition 1>
  - <condition 2>

INPUTS:
  - <input 1>: <type, source>
  - <input 2>: <type, source>

PROCEDURE:
  1. <step>
  2. <step>

OUTPUTS:
  - <output 1>: <type, destination>

CERTIFICATION HOOKS:
  - <hook>: <what gets certified, by which Stage F method>

FAILURE MODES:
  - F<n>: <symptom> → <mitigation>

INTEGRATION:
  - Invoked by: <sub-agent or orchestrator>
  - Operationalized by tools: <T1, T2, ...> (see TOOLING.md)
  - Outputs feed: <sub-agent or stage>
```

---

## S1 — ODI Pre-Check

```yaml
skill_id: S1
name: ODI Pre-Check
version: 0.1
lineage: ABSUBEST v3.1 — Patch P1 (v3.0.1)

TRIGGER CONDITIONS:
  - Any new task received by the orchestrator, before any other processing.
  - Excluded: tasks already classified existential-risk (P0b); those skip S1.

INPUTS:
  - purpose P (informal or formal)
  - context C = (K, R, T)
  - stakeholder list (for consensus check)

PROCEDURE:
  1. HARM CHECK → set w_M ≥ 2 if Yes
  2. SCALE CHECK → set w_B ≥ 2 if Yes
  3. REVERSIBILITY CHECK → set w_I ≥ 5 if No
  4. CHARACTERIZABILITY CHECK → declare coverage class
  5. CONSENSUS CHECK → set multi-agent flag if No
  6. ROUTING RULE → Lite / Express / Full

OUTPUTS:
  - Pre-Check record (5 answers, mandatory floors, routing)
  - Coverage class declaration (computable / heuristic)
  - Multi-agent flag (if set)

CERTIFICATION HOOKS:
  - Pre-Check record archived in declaration (P13 hash includes it)
  - Routing decision traceable to mandatory floors (audit-ready)

FAILURE MODES:
  - F14 ODI gaming → floors immutable in reference impl; manual users sign
  - F13 Bureaucratic paralysis → crisp Yes/No; deterministic routing

INTEGRATION:
  - Invoked by: Meta-Calibrator sub-agent (step 3 of decision sequence)
  - Operationalized by: T1 (odi_precheck.py), MCP-1 (absubest-meta)
  - Outputs feed: ODI computation (S1 → ODI calculator → blueprint generator)
```

---

## S2 — Moral Screen (Consequentialist + Deontological)

```yaml
skill_id: S2
name: Moral Screen
version: 0.1
lineage: ABSUBEST v3.1 — Patches P6 (v3.0.1) + P9 (v3.1)

TRIGGER CONDITIONS:
  - After S1 (ODI Pre-Check) completes, before any optimization begins
  - Re-triggered on mid-run ODI escalation (P10.2)

INPUTS:
  - purpose P (formal or informal)
  - moral screen checklist (P6 + P6b + P0b)

PROCEDURE:
  P6 (Consequentialist):
    1. Does P risk violating fundamental rights? → FAIL if yes
    2. Does P risk severe harm to identifiable populations? → FAIL if yes
    3. Does P undermine democratic processes? → FAIL if yes
    4. Does P risk irreversible ecological destruction? → FAIL if yes
    5. Does P concentrate power without accountability? → FAIL if yes
    6. Does P violate ratified international law? → FAIL if yes
  P6b (Deontological, run after P6 passes):
    1. Does P treat persons merely as means? → FAIL if yes
    2. Does P require deception/manipulation? → FAIL if yes
    3. Does P violate a categorical duty? → FAIL if yes
    4. Does P fail the Kantian universal-law test? → FAIL if yes
    5. Does P fail the Rawlsian veil-of-ignorance test? → FAIL if yes
  P0b (Existential-Risk, run before P1):
    1. Could failure contribute to human extinction? → ESCALATE if yes
    2. Could failure cause permanent civilizational collapse? → ESCALATE if yes
    3. Could failure cause unrecoverable moral-value loss? → ESCALATE if yes
    4. Could failure create unaligned superintelligence? → ESCALATE if yes

OUTPUTS:
  - Moral Screen Record (P6: PASS/FAIL, P6b: PASS/FAIL, P0b: N/A/ESCALATED)
  - If FAIL: diagnostic with which item(s) failed
  - If ESCALATED: handoff to external review board

CERTIFICATION HOOKS:
  - Moral Screen Record archived in declaration (P13 hash)
  - Hard-refusal audit trail (regulator-ready)

FAILURE MODES:
  - F19 Consequentialist-only screen → mitigated by P6b addition
  - Purpose reframing to evade screen → mitigated by re-screening on Purpose Evolution

INTEGRATION:
  - Invoked by: Meta-Calibrator sub-agent (step 2 of decision sequence)
  - Operationalized by: T2 (moral_screen.py), MCP-1
  - Outputs feed: ODI Pre-Check (if P0b passes) or HALT (if P6/P6b fail)
```

---

## S3 — Purpose Crystallization & Utility Construction

```yaml
skill_id: S3
name: Purpose Crystallization
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C1 + A+.1/A+.2/A+.3

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
```

---

## S4 — Constraint Ontology & Liberation

```yaml
skill_id: S4
name: Constraint Ontology
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C2 + B+ Coverage Monotonicity

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
```

---

## S5 — Dimension Derivation + Bias Disclosure

```yaml
skill_id: S5
name: Dimension Derivation + Bias Disclosure
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C3 + C.bias + Patch P5

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
```

---

## S6 — Generative Coverage (Minimal)

```yaml
skill_id: S6
name: Generative Coverage (Minimal)
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C4 + Patch P8

TRIGGER CONDITIONS:
  - After S5 (Stage C) completes
  - Coverage class = Heuristic (declared in S1)

INPUTS:
  - purpose P, utility U, constraints X̃
  - embedding model E (default: sentence-transformers/all-MiniLM-L6-v2)
  - diversity budget N_candidates
  - concept library C (optional)

PROCEDURE:
  1. SEED GENERATION (20% of budget): k₀ = 0.2·N candidates via few-shot prompting with high diversity (temperature 1.2)
  2. DIVERSITY-FILTERED EXPANSION (60% of budget): for each new candidate, embed; compute min distance to existing set; prompt for "far from" most isolated candidates; add if min_distance > θ (default 0.3)
  3. CONCEPT COVERAGE BOOST (20% of budget): for each concept c ∈ C not represented, generate 1 candidate explicitly instantiating c
  4. SATURATION CHECK: stop early if 3 consecutive batches yield < 5% new clusters (DBSCAN ε=0.4, min_samples=2)

OUTPUTS:
  - Candidate set S (size ≤ N)
  - Coverage report:
    - regime: "heuristic"
    - method: "Generative Coverage v3.1"
    - clusters_found: N
    - concept_coverage: X%
    - saturation_achieved: Y/N
    - residual_risk: "unquantified"

CERTIFICATION HOOKS:
  - Coverage report archived in declaration
  - Residual risk labeled "unquantified" (mandatory for heuristic-coverage)

FAILURE MODES:
  - Coverage saturation false-positive → mitigated by DBSCAN cluster count + concept coverage cross-check
  - LLM diversity collapse → mitigated by temperature 1.2 + "far from" prompting

INTEGRATION:
  - Invoked by: Stage-Executor-D sub-agent
  - Operationalized by: T6 (generative_coverage.py), Pgrm-2 (absubest-solver), MCP-2
  - Outputs feed: Stage E (full-spectrum evaluation on S, D, M)
```

---

## S7 — Full-Spectrum Evaluation

```yaml
skill_id: S7
name: Full-Spectrum Evaluation
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C5 + E+ Time-Consistency Hook

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
```

---

## S8 — Optimality Certification (Honest Residual Risk)

```yaml
skill_id: S8
name: Optimality Certification
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C6 + F+ Honest Residual Risk + Patch P11

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
```

---

## S9 — Transcendence Engine

```yaml
skill_id: S9
name: Transcendence Engine
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C8

TRIGGER CONDITIONS:
  - Stage F certification fails OR residual gap > threshold

INPUTS:
  - certificate gap, diagnosed source

PROCEDURE:
  1. Decompose gap into source:
     - Coverage gap (some equivalence class of X unexplored)
     - Dimensional gap (some value dimension omitted from U)
     - Constraint gap (some challengeable constraint unchallenged)
     - Knowledge gap (some relevant fact unknown)
     - Formalization gap (U does not capture stated purpose)
     - Scale gap (cross-scale coherence failure)
  2. Apply corresponding transcendence operator:
     - OP_COV → Stage D' targeted expansion
     - OP_DIM → Stage A' re-derive U with missing dimension
     - OP_CON → Stage B' re-challenge with liberated space
     - OP_KNO → directed research (hypothesis, experimentation, literature)
     - OP_FOR → Stage A re-crystallize purpose
     - OP_SCL → re-enter at different magnitude
  3. Re-run CERTIFY on enhanced solution

OUTPUTS:
  - Enhanced context (U', X̃', K') for next iteration
  - Transcendence log (operator, gap source, action taken)

CERTIFICATION HOOKS:
  - Transcendence log archived in declaration
  - Iteration count and Δ_n tracked

FAILURE MODES:
  - Operator misapplication → mitigated by gap-source decomposition requirement
  - Infinite transcendence loop → mitigated by Layer 2 termination criteria (Δ_n < τ_Δ AND c_n ≥ c_target)

INTEGRATION:
  - Invoked by: Stage-Executor-G sub-agent
  - Operationalized by: T9 (transcend.py), MCP-2
  - Outputs feed: re-enter at appropriate earlier stage (A/B/C/D as indicated by operator)
```

---

## S10 — Verification & Immortalization

```yaml
skill_id: S10
name: Verification & Immortalization
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C9 (verification)

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
```

---

## S11 — Counter-Optimizer Portfolio Assembly

```yaml
skill_id: S11
name: Counter-Optimizer Portfolio Assembly
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C7 + Patches P4 + P11

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
```

---

## S12 — Declaration Drafting (Two-Tier + Comparability)

```yaml
skill_id: S12
name: Declaration Drafting
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C9 (declaration) + Patches P7 + P13

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
```

---

## S13 — Bias Steward (P5 + P14)

```yaml
skill_id: S13
name: Bias Steward
version: 0.1
lineage: ABSUBEST v3.1 — Patches P5 + P14

TRIGGER CONDITIONS:
  - During S5 (Stage C bias disclosure) for budget allocation
  - During self-application tasks (P14)
  - Veto authority over declarations

INPUTS:
  - bias inventory (8 biases from v3.1 Part 7)
  - declaration draft (for veto review)
  - self-application flag (if task is self-app)

PROCEDURE:
  1. Inventory biases (consequentialist, Western-analytic, computability, single-agent, English-language, formalization-as-virtue, anthropocentric, present-date)
  2. For each bias: assess whether it distorts the current process
  3. P5 Bias Correction Budget (mandatory ODI ≥ 7):
     - Allocate resources across perspective panel / co-design / tradition consultation / red-team
     - If budget = $0 for ODI ≥ 7: declaration MUST state "residual distortion likely"
  4. P14 Self-Application Bias Correction (if self-app):
     - 20% of self-app resources to bias correction
     - For each distorting bias: spawn persona from unaffected tradition
     - Persona reviews process and flags distortions
     - Mandatory external review every 2 versions (P14.4)
  5. Veto authority: if bias distortion is severe and uncorrected, veto declaration

OUTPUTS:
  - Bias inventory record
  - Bias Correction Budget allocation (or "insufficient" flag)
  - Self-application bias correction log (if self-app)
  - Veto decision (if applicable)

CERTIFICATION HOOKS:
  - Bias audit archived in declaration
  - Veto (if issued) blocks declaration finalization

FAILURE MODES:
  - F18 Bias disclosure as absolution → mitigated by mandatory budget for ODI ≥ 7
  - F24 Self-application bias unspecified → mitigated by P14 protocol

INTEGRATION:
  - Invoked by: Bias-Steward sub-agent (independent of Stage-Executors)
  - Operationalized by: T13 (bias_steward.py), Pgrm-6 (absubest-bias-audit), MCP-6
  - Outputs feed: S12 (declaration), with veto authority
```

---

## S14 — State Persistence (P12)

```yaml
skill_id: S14
name: State Persistence
version: 0.1
lineage: ABSUBEST v3.1 — Patch P12

TRIGGER CONDITIONS:
  - Macro-tasks (estimated duration > single session)
  - All tasks (for checkpoint/resume capability)

INPUTS:
  - task_id
  - current state (P, U, C, ODI, blueprint, iteration, x_n, certificate, portfolio state, insight log, drift scores, triggers)

PROCEDURE:
  1. State file: /home/z/absubest_state/<task_id>.json
  2. Checkpoint protocol:
     - After each Stage completion: write state file
     - After each iteration boundary: write + verify integrity (SHA-256 hash)
     - Before session termination: write + emit resumption token
  3. Resumption protocol:
     - New session reads state file (if task_id provided)
     - Integrity verified (hash check)
     - Time-Consistency Monitor re-elicits preferences (drift check across sessions)
     - Resume from last checkpoint
  4. Macro-task governance:
     - Tasks > 7 days: appointed human task steward
     - Tasks > 30 days: ethical review board check-in per iteration
     - Tasks > 90 days: full re-validation of Moral Screen + Pre-Check

OUTPUTS:
  - State file (JSON with hash)
  - Resumption token (task_id, state_file path, last_checkpoint, steward_required)
  - Integrity verification result

CERTIFICATION HOOKS:
  - State file integrity check mandatory before resumption
  - Resumption token archived in declaration

FAILURE MODES:
  - F22 No state persistence for macro-tasks → mitigated by P12 protocol
  - F30 State file corruption → mitigated by 3-copy replication + periodic integrity checks

INTEGRATION:
  - Invoked by: State-Persistence-Manager sub-agent
  - Operationalized by: T14 (state_persist.py), Pgrm-5 (absubest-state-server), MCP-5
  - Outputs feed: orchestrator (for resume); declaration archive (for resumption token)
```

---

## S15 — Cross-Framework Comparability Registry

```yaml
skill_id: S15
name: Cross-Framework Comparability Registry
version: 0.1
lineage: ABSUBEST v3.1 — Patch P13

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
```

---

## Skill Coverage Matrix

| Core Process / Patch | Addressed By Skill(s) | Coverage |
|---------------------|----------------------|----------|
| C1 Purpose Formalization | S3 | Full |
| C2 Constraint Ontology | S4 | Full |
| C3 Dimension Derivation | S5 | Full |
| C4 Solution-Space Coverage | S6 | Full |
| C5 Full-Spectrum Evaluation | S7 | Full |
| C6 Optimality Certification | S8 | Full |
| C7 Counter-Optimization | S11 | Full |
| C8 Transcendence | S9 | Full |
| C9 Verification & Declaration | S10, S12 | Full |
| C10 Meta-Control | S1 (entry), Meta-Opt-Loop sub-agent | Full |
| C11 Purpose Evolution | S3 (A+.3 hooks) | Full |
| C12 Time-Consistency Monitoring | S7 (E+ hook) | Full |
| P1 ODI Pre-Check | S1 | Full |
| P2 Express Mode | Meta-Calibrator sub-agent | Full |
| P3 Fast-Track Tier 4 | S3 (A+.2) | Full |
| P4 Portfolio Diversity Metric | S11 | Full |
| P5 Bias Correction Budget | S5, S13 | Full |
| P6 Consequentialist Moral Screen | S2 | Full |
| P7 Uncertainty Sign-off | S12 | Full |
| P8 Minimal Generative Coverage | S6 | Full |
| P9 Deontological Moral Screen | S2 | Full |
| P10 Existential-Risk + Mid-Run Escalation | S2 (P0b), Meta-Opt-Loop sub-agent (P10.2) | Full |
| P11 Portfolio Diversity Fallback | S11 | Full |
| P12 State Persistence | S14 | Full |
| P13 Cross-Framework Comparability | S12, S15 | Full |
| P14 Self-Application Bias Correction | S13 | Full |

All 12 core processes and all 14 patches have full skill coverage.

---

*SKILLS.md v0.1 — generated 2026-06-22 by ABSUBEST v3.1 Deployment #2.*
