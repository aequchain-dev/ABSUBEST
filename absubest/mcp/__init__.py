"""
ABSUBEST MCP (Model Context Protocol) servers.

Tier 3 tooling: JSON-RPC 2.0 over stdio for integration with
LLM agents, editors, and external tooling.

Servers:
    MCP-1: absubest_meta.py       — Orchestrator, ODI, blueprint
    MCP-2: absubest_stage.py      — Stage A–H pipeline executor
    MCP-3: absubest_counter_opt.py — Counter-optimizer portfolio
    MCP-4: absubest_archive.py    — Declaration archive & registry
    MCP-5: absubest_state.py      — State persistence & checkpoints
    MCP-6: absubest_bias.py       — Bias detection & correction
"""

from .absubest_meta import (
    mcp,
    ping,
    optimize,
    resume,
    registry_list,
    registry_get,
    bias_audit,
    reverify,
    main as serve_meta,
)

from .absubest_stage import (
    MCP2Handler,
    serve_stdio as serve_stage,
    serve_stdio_forever as serve_stage_forever,
)

from .absubest_counter_opt import (
    MCP3Handler,
    serve_stdio as serve_counter_opt,
    serve_stdio_forever as serve_counter_opt_forever,
)

from .absubest_archive import (
    MCP4Handler,
    serve_stdio_forever as serve_archive,
)

from .absubest_state import (
    MCP5Handler,
    serve_stdio_forever as serve_state,
)

from .absubest_bias import (
    MCP6Handler,
    serve_stdio_forever as serve_bias,
)

__all__ = [
    # MCP-1
    "mcp",
    "ping",
    "optimize",
    "resume",
    "registry_list",
    "registry_get",
    "bias_audit",
    "reverify",
    "serve_meta",
    # MCP-2
    "MCP2Handler",
    "serve_stage",
    "serve_stage_forever",
    # MCP-3
    "MCP3Handler",
    "serve_counter_opt",
    "serve_counter_opt_forever",
    # MCP-4
    "MCP4Handler",
    "serve_archive",
    # MCP-5
    "MCP5Handler",
    "serve_state",
    # MCP-6
    "MCP6Handler",
    "serve_bias",
]
