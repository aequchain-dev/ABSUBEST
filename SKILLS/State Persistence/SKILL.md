---
skill_id: S14
name: State Persistence
version: 0.1
lineage: ABSUBEST v3.1 — Patch P12
---
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
