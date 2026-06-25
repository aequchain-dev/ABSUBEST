---
skill_id: S1
name: ODI Pre-Check
version: 0.1
lineage: ABSUBEST v3.1 — Patch P1 (v3.0.1)
compatibility: opencode
---
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
