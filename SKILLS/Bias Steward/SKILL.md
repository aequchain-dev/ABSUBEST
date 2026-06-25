---
skill_id: S13
name: Bias Steward
version: 0.1
lineage: ABSUBEST v3.1 — Patches P5 + P14
---
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
