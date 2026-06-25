"""
ABSUBEST CLI — Entrypoint for `absubest run`, `absubest resume`, etc.

Usage:
    absubest run --purpose "select best routing algorithm" [--context @ctx.json] [--odi-weights default]
    absubest resume --task-id <task_id>
    absubest registry query --purpose-hash <hash>
    absubest registry compare <decl_a> <decl_b>
    absubest bias audit --task-id <task_id>
    absubest reverification schedule --task-id <task_id> --trigger <trigger_name>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Sub-command: run
# ---------------------------------------------------------------------------

def cmd_run(args: argparse.Namespace) -> int:
    """Run ABSUBEST on a stated purpose."""
    from absubest import ABSUBEST

    context: dict[str, Any] = {}
    if args.context:
        ctx_path = Path(args.context).expanduser()
        if ctx_path.suffix == ".json":
            with open(ctx_path) as f:
                context = json.load(f)
        else:
            # treat as inline JSON file
            with open(ctx_path) as f:
                context = json.load(f)

    odi_weights = args.odi_weights or "default"

    ab = ABSUBEST(
        knowledge_horizon=context.get("K", "2026-06-22"),
        resource_budget=context.get("R", "unlimited"),
        time_budget=context.get("T", "unlimited"),
        task_id=args.task_id,
    )

    result = ab.optimize(
        purpose=args.purpose,
        odi_weights=odi_weights,
    )

    print(result.format())
    return 0


# ---------------------------------------------------------------------------
# Sub-command: resume
# ---------------------------------------------------------------------------

def cmd_resume(args: argparse.Namespace) -> int:
    """Resume a macro-task from a saved checkpoint."""
    from absubest import ABSUBEST

    ab = ABSUBEST(state_persistence=True)
    result = ab.resume(task_id=args.task_id)
    print(result.format())
    return 0


# ---------------------------------------------------------------------------
# Sub-command: registry
# ---------------------------------------------------------------------------

def cmd_registry(args: argparse.Namespace) -> int:
    """Query or compare declarations in the cross-framework registry."""
    from absubest.skills.s15_registry import ABSUBESTRegistry

    registry = ABSUBESTRegistry()

    if args.registry_action == "query":
        results = registry.query(purpose_hash=args.purpose_hash)
        for r in results:
            print(json.dumps(r, indent=2, default=str))
    elif args.registry_action == "compare":
        comparison = registry.compare(args.decl_a, args.decl_b)
        print(json.dumps(comparison, indent=2, default=str))
    else:
        print(f"Unknown registry action: {args.registry_action}")
        return 1
    return 0


# ---------------------------------------------------------------------------
# Sub-command: bias
# ---------------------------------------------------------------------------

def cmd_bias(args: argparse.Namespace) -> int:
    """Audit bias for a completed task."""
    from absubest.skills.s13_bias import bias_inventory

    report = bias_inventory(task_id=args.task_id)
    print(json.dumps(report, indent=2, default=str))
    return 0


# ---------------------------------------------------------------------------
# Sub-command: reverification
# ---------------------------------------------------------------------------

def cmd_reverification(args: argparse.Namespace) -> int:
    """Schedule re-verification for a task."""
    from absubest.skills.s15_registry import ABSUBESTRegistry

    registry = ABSUBESTRegistry()
    registry.schedule_reverification(
        task_id=args.task_id,
        trigger=args.trigger,
    )
    print(f"Re-verification scheduled for task {args.task_id} (trigger: {args.trigger})")
    return 0


# ---------------------------------------------------------------------------
# Main dispatcher
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="absubest",
        description="ABSUBEST Framework — meta-optimizer for any explicit purpose",
    )
    parser.add_argument("--version", action="version", version="absubest 0.1.0")

    sub = parser.add_subparsers(dest="command", required=True)

    # run
    p_run = sub.add_parser("run", help="Run ABSUBEST on a purpose")
    p_run.add_argument("--purpose", "-p", required=True, help="Purpose statement")
    p_run.add_argument("--context", "-c", help="Path to context JSON file (@ctx.json)")
    p_run.add_argument("--odi-weights", "-w", help="ODI weight profile (default / path)")
    p_run.add_argument("--task-id", "-t", help="Task identifier for state persistence")
    p_run.set_defaults(func=cmd_run)

    # resume
    p_resume = sub.add_parser("resume", help="Resume a macro-task")
    p_resume.add_argument("--task-id", "-t", required=True, help="Task identifier")
    p_resume.set_defaults(func=cmd_resume)

    # registry
    p_reg = sub.add_parser("registry", help="Query or compare declarations")
    reg_sub = p_reg.add_subparsers(dest="registry_action", required=True)

    p_reg_query = reg_sub.add_parser("query", help="Query declarations by purpose hash")
    p_reg_query.add_argument("--purpose-hash", required=True, help="SHA-256 purpose hash")
    p_reg_query.set_defaults(func=cmd_registry)

    p_reg_cmp = reg_sub.add_parser("compare", help="Compare two declarations")
    p_reg_cmp.add_argument("decl_a", help="First declaration ID")
    p_reg_cmp.add_argument("decl_b", help="Second declaration ID")
    p_reg_cmp.set_defaults(func=cmd_registry)

    # bias
    p_bias = sub.add_parser("bias", help="Bias audit operations")
    bias_sub = p_bias.add_subparsers(dest="bias_action", required=True)
    p_bias_audit = bias_sub.add_parser("audit", help="Audit bias for a task")
    p_bias_audit.add_argument("--task-id", "-t", required=True)
    p_bias_audit.set_defaults(func=cmd_bias)

    # reverification
    p_rev = sub.add_parser("reverification", help="Schedule re-verification")
    rev_sub = p_rev.add_subparsers(dest="rev_action", required=True)
    p_rev_sched = rev_sub.add_parser("schedule", help="Schedule re-verification")
    p_rev_sched.add_argument("--task-id", "-t", required=True)
    p_rev_sched.add_argument("--trigger", required=True, help="Re-verification trigger name")
    p_rev_sched.set_defaults(func=cmd_reverification)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        return args.func(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
