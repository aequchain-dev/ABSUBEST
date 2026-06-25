# ABSUBEST — Absolute Best Framework

**Given any explicit purpose, dynamically synthesizes and executes the optimal optimization process for that purpose.**

| Field | Value |
|---|---|
| Version | 0.1.0 (Deployment #2) |
| Framework | ABSUBEST v3.1 |
| Status | Alpha — internal deployment |
| Expiration | 2026-12-22 (re-verification trigger) |
| ODI | 9.53 (Deployment #2) |

## Quick Start

```bash
# Install from source
pip install -e .

# Run the pipeline
absubest run --purpose "Design a low-cost solar water pump for rural Senegal"

# With context file
absubest run --purpose "Optimize supply chain" --context context.json

# Resume a previous task
absubest resume --task-id abc123

# List archived declarations
absubest registry list

# Get a specific declaration
absubest registry get --id decl-abc123

# Trigger re-verification
absubest reverify --registry-id decl-abc123

# Bias audit
absubest bias --task-id abc123
```

## Architecture

```
absubest/
├── __init__.py          # Package init, version, main exports
├── cli.py              # CLI entrypoint (absubest run/resume/registry/...)
├── schema.py           # JSON Schema definitions for all protocol types
│
├── core/
│   ├── orchestrator.py     # ABSUBEST class — 14-stage pipeline
│   ├── meta_calibrator.py  # Layer 0 — ODI pre-check → blueprint
│   ├── meta_opt_loop.py    # Layer 2 — convergence monitoring
│   │
│   └── sub_agents/
│       ├── stage_executor_a.py         # Purpose crystallization
│       ├── stage_executor_b.py         # Constraint ontology
│       ├── stage_executor_c.py         # Dimension derivation
│       ├── stage_executor_d.py         # Solution-space construction
│       ├── stage_executor_e.py         # Full-spectrum evaluation
│       ├── stage_executor_f.py         # Optimality certification
│       ├── stage_executor_g.py         # Transcendence
│       ├── stage_executor_h.py         # Verification
│       ├── counter_opt_manager.py      # Counter-optimizer portfolio
│       ├── declaration_archivist.py    # Draft + persist declarations
│       ├── bias_steward.py             # Bias correction
│       └── state_persistence_manager.py # Checkpoint/resume
│
├── skills/
│   ├── s1_odi_precheck.py    # ODI Pre-Check (P1)
│   ├── s2_moral_screen.py    # Moral screens (P6, P6b, P0b)
│   ├── s3_purpose.py         # Purpose crystallization (A+.1/A+.2/A+.3)
│   ├── s4_constraint.py      # Constraint ontology (6-class)
│   ├── s5_dimension.py       # Dimension derivation + bias (C.bias)
│   ├── s6_coverage.py        # Solution-space coverage (P8)
│   ├── s7_evaluate.py        # Full-spectrum evaluation (6 methods)
│   ├── s8_certify.py         # Optimality certification
│   ├── s9_transcend.py       # Transcendence operators (OP_COV–OP_SCL)
│   ├── s10_verify.py         # Multi-method verification
│   ├── s11_portfolio.py      # Counter-optimizer portfolio (P4)
│   ├── s12_declare.py        # Two-tier declaration drafting
│   ├── s13_bias.py           # Bias steward (P5, P14)
│   ├── s14_state.py          # State persistence (P12)
│   └── s15_registry.py       # Declaration registry (P13)
│
└── mcp/
    └── absubest_meta.py      # MCP-1 JSON-RPC 2.0 over stdio server
```

## Pipeline Stages (Default Full, ODI ≥ 7)

1. **Intake** — receive purpose P, context C = (K, R, T); assign task_id
2. **Existential-Risk Check** (P10.1 / P0b) — escalate if triggered
3. **Moral Screens** (P6, P6b) — halt on failure
4. **ODI Pre-Check** (P1) — 5-question calibration → Lite/Express/Full route
5. **Blueprint Generation** (Layer 0) — pipeline configuration
6. **Purpose Crystallization** (Stage A) — utility function U, coherence verification
7. **Constraint Ontology** (Stage B) — 6-class classification, liberation
8. **Dimension Derivation** (Stage C) — concept algebra, bias disclosure
9. **Solution-Space Construction** (Stage D) — candidate generation, coverage
10. **Full-Spectrum Evaluation** (Stage E) — 6 evaluation methods
11. **Optimality Certification** (Stage F) — escalating certification
12. **Counter-Optimization** (Layer 2) — diversity-gated portfolio (ODI ≥ 7)
13. **Transcendence** (Stage G) — gap-closing operators
14. **Verification & Declaration** (Stage H) — two-tier, archived

## MCP-1 Protocol

The MCP-1 server provides JSON-RPC 2.0 over stdio:

```bash
# One-shot mode (reads single request from stdin)
echo '{"jsonrpc":"2.0","id":"1","method":"ping","params":{}}' | absubest-mcp

# Forever mode (continuous)
echo '{"jsonrpc":"2.0","id":"1","method":"optimize","params":{"purpose":"test"}}' | absubest-mcp --forever
```

### Methods

| Method | Description |
|---|---|
| `ping` | Health check → `{"pong": true, "version": "0.1.0"}` |
| `optimize` | Run ABSUBEST pipeline on a purpose |
| `resume` | Resume a checkpointed task |
| `registry_list` | List archived declarations |
| `registry_get` | Get declaration by ID |
| `bias_audit` | Audit bias for a task |
| `reverify` | Re-run verification for a declaration |

## Declarations

Every ABSUBEST optimization produces a **two-tier declaration**:

- **Epistemic declaration** — formal bounds, certification type, residual risk, counter-optimizer concessions, diversity score, bias audit
- **Ceremonial declaration** — narrative summary, scores, next steps

Declarations are archived in the `~/.absubest/registry/` SQLite database with **P13 comparability headers** (SHA-256 framework + declaration hashes).

## ODI Calibration

The **Optimality-Directed Investment** (ODI) score (0–10) determines pipeline rigor:

| ODI | Route | Stages | Counter-Opt |
|-----|-------|--------|-------------|
| 0–3 | Lite | A–F | Optional |
| 4–6 | Express | A–H (simplified) | Optional |
| 7–10 | Full | All (maximum rigor) | Mandatory |

## Hard Refusals

The pipeline **halts** and returns a diagnostic when:
- P6 (consequentialist) moral screen fails
- P6b (deontological) moral screen fails
- P0b existential-risk trigger without external review sign-off
- ODI Pre-Check is incomplete
- Counter-optimizer portfolio diversity D(Π) < 0.3
- Bias correction budget is zero for ODI ≥ 7

## License

MIT OR Apache-2.0

---

*This is* The Absolute Best *as a regulative ideal (Stratum III, Kantian sense). Every declaration is indexical — bounded by context C, date D, and knowledge horizon K.*
