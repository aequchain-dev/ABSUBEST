---
skill_id: S2
name: Moral Screen
version: 0.1
lineage: ABSUBEST v3.1 — Patches P6 (v3.0.1) + P9 (v3.1)
---
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
