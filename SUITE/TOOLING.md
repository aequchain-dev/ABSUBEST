# TOOLING.md — ABSUBEST-Exactor v0.1
## Tooling Environment: 4 Tiers Operationalizing the Skills

> **Lineage**: ABSUBEST v3.1 → Deployment #2
> **Structure**: 4 tiers (Local Scripts / Programs / MCPs / Plugins), each with independent release cadence
> **Status**: specification complete; build per Implementation Plan Phase 1–3
> **License**: MIT or Apache 2.0 (constraint C11: reproducible at zero cost)

Every tool below is referenced by at least one skill (see `SKILLS.md`) and at least one sub-agent (see `AGENT.md`). Cohesion (D4 of U(design)) requires that every skill has at least one operationalizing tool, and every sub-agent invokes at least one skill — verified.

---

## Tier 1 — Local Scripts (Python Modules)

Tier 1 tools are Python modules importable by the orchestrator. Pure Python plus open-source libraries. **Built in Phase 1 (Week 1–4)**.

| Tool | Skill(s) | Purpose | Dependencies |
|------|----------|---------|--------------|
| T1 `odi_precheck.py` | S1 | Run 5-question Pre-Check; route to Lite/Express/Full | — |
| T2 `moral_screen.py` | S2 | Run P6 + P6b + P0b checks on purpose P | — |
| T3 `purpose_crystallize.py` | S3 | Elicit U from P; coherence verification | — |
| T4 `constraint_ontology.py` | S4 | Classify constraints; liberation protocol | — |
| T5 `dimension_derive.py` | S5 | Derive dimensions; bias disclosure | — |
| T6 `generative_coverage.py` | S6 | Minimal Generative Coverage v3.1 | sentence-transformers, scikit-learn, LLM API |
| T7 `evaluate.py` | S7 | Multi-method scoring of candidates | depends on method |
| T8 `certify.py` | S8 | Optimality certification with residual risk | optionally Z3, Lean |
| T9 `transcend.py` | S9 | Apply transcendence operators | — |
| T10 `verify.py` | S10 | Multi-method verification | depends on method |
| T11 `portfolio_assemble.py` | S11 | Counter-opt portfolio assembly + diversity | — |
| T12 `declare.py` | S12 | Two-tier declaration drafting + P13 header | — |
| T13 `bias_steward.py` | S13 | Bias inventory + correction + veto | — |
| T14 `state_persist.py` | S14 | P12 checkpoint/resume | — |
| T15 `registry.py` | S15 | P13 cross-framework registry | sqlite3 (stdlib) |

### Python Package Structure

```
absubest/
├── __init__.py              # exports ABSUBEST class
├── core/
│   ├── orchestrator.py      # ABSUBEST-Exactor main loop
│   ├── meta_calibrator.py   # Layer 0
│   ├── meta_opt_loop.py     # Layer 2
│   └── sub_agents/
│       ├── stage_a.py       # Stage-Executor-A
│       ├── stage_b.py
│       ├── stage_c.py
│       ├── stage_d.py
│       ├── stage_e.py
│       ├── stage_f.py
│       ├── stage_g.py
│       ├── stage_h.py
│       ├── counter_opt_manager.py
│       ├── bias_steward.py
│       ├── declaration_archivist.py
│       └── state_persistence_manager.py
├── skills/                  # one module per skill
│   ├── s1_odi_precheck.py   # T1
│   ├── s2_moral_screen.py   # T2
│   ├── s3_purpose.py        # T3
│   ├── s4_constraint.py     # T4
│   ├── s5_dimension.py      # T5
│   ├── s6_coverage.py       # T6
│   ├── s7_evaluate.py       # T7
│   ├── s8_certify.py        # T8
│   ├── s9_transcend.py      # T9
│   ├── s10_verify.py        # T10
│   ├── s11_portfolio.py     # T11
│   ├── s12_declare.py       # T12
│   ├── s13_bias.py          # T13
│   ├── s14_state.py         # T14
│   └── s15_registry.py      # T15
├── mcp/                     # MCP servers (Tier 3)
│   ├── absubest_meta.py     # MCP-1
│   ├── absubest_stage.py    # MCP-2
│   ├── absubest_counter.py  # MCP-3
│   ├── absubest_archive.py  # MCP-4
│   ├── absubest_state.py    # MCP-5
│   └── absubest_bias.py     # MCP-6
└── cli.py                   # `absubest` entrypoint
```

### CLI Surface

```bash
# Run ABSUBEST on a purpose
absubest run --purpose "select best routing algorithm" --context @ctx.json

# Resume a macro-task
absubest resume --task-id my_macro_task_001

# Query the declaration registry
absubest registry query --purpose-hash <hash>
absubest registry compare <decl_a> <decl_b>

# Bias audit
absubest bias audit --task-id my_task

# Schedule re-verification
absubest reverification schedule --task-id my_task --trigger external_deployment
```

---

## Tier 2 — Programs (Standalone Executables)

Tier 2 tools are standalone programs (Python CLIs or compiled binaries) for heavier operations. May have external service dependencies (Z3, Gurobi, Lean). **Built in Phase 2 (Week 4–12)**.

| Program | Purpose | Built On | Status |
|---------|---------|----------|--------|
| Pgrm-1 `absubest-prover` | Stage F formal proofs (Pareto, upper-bound, attainment) | Lean 4 + Coq + Why3 + Z3 + CVC5 | Spec; build Phase 2 |
| Pgrm-2 `absubest-solver` | Stage D symbolic search; Stage E optimization | OR-Tools + Gurobi (optional) + CMA-ES + scipy | Spec; build Phase 2 |
| Pgrm-3 `absubest-counter-opt` | Counter-optimizer portfolio runtime | Custom + LLM APIs + solver hooks | Spec; build Phase 2 |
| Pgrm-4 `absubest-archive` | Declaration archive with comparability registry | SQLite + JSON-LD | Spec; build Phase 1 (lite) → Phase 2 (full) |
| Pgrm-5 `absubest-state-server` | P12 state persistence daemon | FastAPI + SQLite | Spec; build Phase 2 |
| Pgrm-6 `absubest-bias-audit` | Bias inventory audit + P14 self-app correction | Custom + LLM red-team | Spec; build Phase 2 |

### Pgrm-1 absubest-prover

```bash
absubest-prover prove --spec spec.lean --method pareto | upper-bound | formal | redundant
absubest-prover check --certificate cert.lean
absubest-prover refute --claim claim.lean
```

- **Inputs**: Lean 4 / Coq / Why3 specification; SMT-LIB for Z3/CVC5
- **Outputs**: proof certificate (machine-checkable) OR refutation OR timeout
- **Failure modes**: proof timeout (mitigation: escalate to statistical bound); specification ambiguity (mitigation: require explicit type annotations)

### Pgrm-2 absubest-solver

```bash
absubest-solver solve --problem problem.lp --solver gurobi | ortools | cma-es | scipy
absubest-solver search --space grammar.json --strategy symbolic | stratified | exhaustive
absubest-solver optimize --fn blackbox.py --method bayesopt | cma-es
```

- **Inputs**: optimization problem (LP/ILP/MILP/CP/QCQP/blackbox)
- **Outputs**: solution + certificate (Gurobi gap; CMA-ES convergence; BayesOpt regret bound)
- **Failure modes**: solver timeout (mitigation: switch to approximate); infeasible (mitigation: return diagnostic for Stage G)

### Pgrm-3 absubest-counter-opt

```bash
absubest-counter-opt assemble --purpose P --baseline x* --portfolio-config config.yaml
absubest-counter-opt run --member <name> --budget 30%
absubest-counter-opt aggregate --portfolio-run <run-id>
absubest-counter-opt diversity --portfolio Π
```

- **Inputs**: purpose, baseline solution, portfolio config (paradigm tags, blind-spot profiles, budgets)
- **Outputs**: concession log per member; diversity score D(Π); aggregate outcome; suspicious-concession flags
- **Failure modes**: member timeout (mitigation: log as inconclusive); strategic concession (mitigation: trace audit + random member injection)

### Pgrm-4 absubest-archive

```bash
absubest-archive insert --declaration decl.json
absubest-archive query --purpose-hash H [--framework-id F]
absubest-archive compare <decl_a> <decl_b>
absubest-archive schedule-reverification --task-id T --trigger <name>
absubest-archive expire --before <date>
```

- **Storage**: SQLite + JSON-LD files for full traces
- **Schema**: comparability header columns + JSON trace blob
- **Failure modes**: contention (mitigation: single-writer pattern); corruption (mitigation: 3-copy replication)

### Pgrm-5 absubest-state-server

```bash
absubest-state-server start --db state.db
absubest-state-server checkpoint --task-id T --state state.json
absubest-state-server resume --task-id T
absubest-state-server integrity-check --task-id T
absubest-state-server emit-token --task-id T
```

- **API**: FastAPI daemon (HTTP/JSON)
- **Storage**: SQLite for state files
- **Failure modes**: daemon crash (mitigation: systemd restart; state is durable); corruption (mitigation: SHA-256 hash per checkpoint)

### Pgrm-6 absubest-bias-audit

```bash
absubest-bias-audit inventory --task-id T
absubest-bias-audit budget --task-id T --allocate perspective:500,redteam:500
absubest-bias-audit self-app-review --version v3.1 --target v3.2
absubest-bias-audit veto --declaration decl.json --reason "..."
```

- **Inputs**: bias inventory template; declaration draft; self-application log
- **Outputs**: bias audit report; budget allocation; veto decision
- **Failure modes**: bias inventory incomplete (mitigation: 8 mandatory checkboxes); veto override abuse (mitigation: veto reason must reference specific bias + distortion)

---

## Tier 3 — MCPs (Model Context Protocol Servers)

Tier 3 tools are MCP servers exposing ABSUBEST operations to any LLM agent that speaks MCP. **Built in Phase 2–3 (Week 4–24)**.

| MCP Server | Exposes | JSON-RPC Methods |
|------------|---------|------------------|
| MCP-1 `absubest-meta` | Meta-Calibrator operations | `odi_precheck`, `compute_odi`, `generate_blueprint`, `declare_coverage_class` |
| MCP-2 `absubest-stage` | Stage A–H execution | `stage_a_crystallize`, `stage_b_ontology`, `stage_c_dimension`, `stage_d_coverage`, `stage_e_evaluate`, `stage_f_certify`, `stage_g_transcend`, `stage_h_verify` |
| MCP-3 `absubest-counter-opt` | Counter-optimizer portfolio | `assemble_portfolio`, `run_member`, `aggregate_concessions`, `diversity_score` |
| MCP-4 `absubest-archive` | Declaration archive + registry | `archive_declaration`, `query_registry`, `compare_declarations`, `schedule_reverification` |
| MCP-5 `absubest-state` | State persistence | `checkpoint`, `resume`, `emit_resumption_token`, `integrity_check` |
| MCP-6 `absubest-bias` | Bias steward operations | `inventory_biases`, `allocate_correction_budget`, `review_self_application`, `veto_declaration` |

### MCP-1 absubest-meta (example JSON-RPC)

```json
{
  "jsonrpc": "2.0",
  "method": "odi_precheck",
  "params": {
    "purpose": "select best routing algorithm for sensor network",
    "context": {"K": "2026-06-22", "R": "2 engineer-weeks", "T": "3 weeks"},
    "stakeholders": ["network-ops", "eng-team"]
  },
  "id": 1
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "answers": ["No", "No", "Yes", "Yes", "Yes"],
    "mandatory_floors": {},
    "routing": "Lite permitted",
    "coverage_class": "computable",
    "multi_agent_flag": false
  },
  "id": 1
}
```

### MCP Integration with LLM Clients

Any MCP-compatible LLM client can connect:

- **Claude Desktop**: `~/.claude/mcp.json` → `{"absubest-meta": {"command": "python", "args": ["-m", "absubest.mcp.absubest_meta"]}}`
- **Cursor**: Settings → MCP → add server
- **VS Code (with Cline)**: `.clinerules/mcp.json`
- **Custom**: any client speaking MCP JSON-RPC over stdio

---

## Tier 4 — Plugins (Integrations)

Tier 4 tools are integrations with existing developer environments. Not required for ABSUBEST to function but reduce adoption friction. **Built in Phase 3 (Week 12–24)**.

| Plugin | Integrates With | Function |
|--------|----------------|----------|
| Plg-1 `absubest-vscode` | VS Code | Sidebar for declarations, state files, bias audits; run ABSUBEST on selected purpose |
| Plg-2 `absubest-jetbrains` | IntelliJ / PyCharm / WebStorm | Same as Plg-1 for JetBrains IDEs |
| Plg-3 `absubest-cli` | POSIX shell | CLI wrapper around Tier 1+2 tools: `absubest run --purpose P --context C` |
| Plg-4 `absubest-github-action` | GitHub Actions | CI hook: every PR triggers ABSUBEST-Lite on the PR's stated purpose |
| Plg-5 `absubest-jupyter` | JupyterLab | Notebook magics: `%absubest run P`, `%absubest declare` |
| Plg-6 `absubest-registry-ui` | Web browser | Web UI for the declaration archive (P13 registry); query, compare, schedule re-verification |

### Plg-1 absubest-vscode (sketch)

Contributes:
- **Sidebar view**: tree of declarations in registry, grouped by purpose_hash
- **Command palette**: `ABSUBEST: Run on Selected Purpose`, `ABSUBEST: Resume Task`, `ABSUBEST: Query Registry`
- **Status bar**: current task_id, iteration count, Δ_n, drift score
- **Editor decorations**: when editing an AGENT.md or SKILLS.md, highlight mandate references and show tooltip with skill spec
- **Settings**: `absubest.mcpServers` (list), `absubest.defaultOdiWeights`, `absubest.registryPath`

### Plg-4 absubest-github-action (sketch)

```yaml
# .github/workflows/absubest.yml
name: ABSUBEST-Lite on PR
on: pull_request
jobs:
  absubest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: absubest/github-action@v0.1
        with:
          purpose: ${{ github.event.pull_request.title }}
          context: |
            K: 2026-06-22
            R: free
            T: 1 hour
          odi-weights: default
          pipeline: lite
```

The action runs ABSUBEST-Lite on the PR's stated purpose and posts the declaration as a comment. If the declaration includes a hard refusal (moral screen fail), the action blocks the PR.

---

## Tool ↔ Skill ↔ Sub-Agent Cross-Reference

| Sub-Agent | Invokes Skills | Operationalized by Tools |
|-----------|---------------|-------------------------|
| Meta-Calibrator | S1, S2 (P0b), S3 (A+.2 Fast-Track) | T1, T2, T3, MCP-1 |
| Stage-Executor-A | S3 | T3, MCP-2 |
| Stage-Executor-B | S4 | T4, MCP-2 |
| Stage-Executor-C | S5 | T5, MCP-2 |
| Stage-Executor-D | S6 | T6, Pgrm-2, MCP-2 |
| Stage-Executor-E | S7 | T7, Pgrm-2, MCP-2 |
| Stage-Executor-F | S8 | T8, Pgrm-1, MCP-2 |
| Stage-Executor-G | S9 | T9, MCP-2 |
| Stage-Executor-H | S10, S12 | T10, T12, Pgrm-4, MCP-2, MCP-4 |
| Counter-Opt-Manager | S11 | T11, Pgrm-3, MCP-3 |
| Meta-Opt-Loop | S1 (re-entry), S7 (E+ hook) | T1, T7 |
| Bias-Steward | S13 | T13, Pgrm-6, MCP-6 |
| Declaration-Archivist | S12, S15 | T12, T15, Pgrm-4, MCP-4 |
| State-Persistence-Manager | S14 | T14, Pgrm-5, MCP-5 |

Cross-reference resolution rate: 100%. Every skill is operationalized by at least one tool. Every sub-agent invokes at least one skill. Cohesion (D4) is satisfied.

---

## Build Status

| Tier | Build Phase | Status |
|------|-------------|--------|
| Tier 1 (Local Scripts) | Phase 1 (Week 1–4) | Spec complete; not yet built |
| Tier 2 (Programs) | Phase 2 (Week 4–12) | Spec complete; not yet built |
| Tier 3 (MCPs) | Phase 2–3 (Week 4–24) | Spec complete; not yet built |
| Tier 4 (Plugins) | Phase 3 (Week 12–24) | Spec complete; not yet built |

See Implementation Plan PDF Part XII for full phase sequencing, dependencies, exit criteria, and risk register.

---

*TOOLING.md v0.1 — generated 2026-06-22 by ABSUBEST v3.1 Deployment #2.*
