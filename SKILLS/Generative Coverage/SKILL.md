---
skill_id: S6
name: Generative Coverage (Minimal)
version: 0.1
lineage: ABSUBEST v3.1 — Core Process C4 + Patch P8
---
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
    - method: "Minimal Generative Coverage v3.1"
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
