"""
MCP-3 Counter-Optimizer — FastMCP Server.

Assembles and runs paradigm-diverse counter-optimizer portfolios
(P4) to stress-test candidate solutions from alternative frameworks.
Includes P11 fallback tiers when portfolio diversity is insufficient.

Tools:
    ping                  → health check
    portfolio_assemble    → Build portfolio Π per P4
    portfolio_run         → Execute all strategies in portfolio
    portfolio_diversity   → Compute diversity metric D(Π)
    portfolio_aggregate   → Aggregate concessions across portfolio
"""

from __future__ import annotations

import logging

from absubest.skills.s11_portfolio import PortfolioAssembler
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger("absubest.mcp.counter_opt")


mcp = FastMCP(
    "absubest-counter-opt",
    instructions="ABSUBEST MCP-3 Counter-Optimizer Server",
)


@mcp.tool()
def ping() -> dict:
    """Health check."""
    return {"pong": True, "server": "absubest-counter-opt"}


@mcp.tool()
def portfolio_assemble(
    purpose: str = "Counter-optimize current best solution",
    best_solution: dict | None = None,
    n_optimizers: int = 5,
    odi: float = 8.0,
) -> dict:
    """Assemble counter-optimizer portfolio Π per P4.

    Args:
        purpose: optimization purpose (default auto-generated)
        best_solution: current best solution to counter-optimize
        n_optimizers: number of counter-optimizer paradigms (default 5)
        odi: ODI score for P11 threshold check
    """
    assembler = PortfolioAssembler()
    portfolio = assembler.assemble(
        purpose=purpose,
        best_solution=best_solution or {},
        n_optimizers=n_optimizers,
    )
    d_val = assembler.diversity_score(portfolio)
    diversity = {"D": d_val}

    if odi >= 7 and d_val < 0.3:
        portfolio["p11_fallback_triggered"] = True
        portfolio["diversity_warning"] = (
            f"D(Π)={d_val:.3f} < 0.3 threshold. "
            f"P11 Tier 3 fallback required."
        )

    return {
        "portfolio": portfolio,
        "n_strategies": len(portfolio.get("optimizers", [])),
        "diversity": diversity,
        "odi": odi,
    }


@mcp.tool()
def portfolio_run(
    portfolio: dict,
) -> dict:
    """Execute all counter-optimizer strategies in the portfolio.

    Args:
        portfolio: The portfolio dict from portfolio_assemble
    """
    assembler = PortfolioAssembler()
    results = assembler.run(portfolio)

    return {
        "results": results,
        "n_concessions": len(results),
        "total_strategies": len(portfolio.get("optimizers", [])),
    }


@mcp.tool()
def portfolio_diversity(
    portfolio: dict | None = None,
) -> dict:
    """Compute diversity metric D(Π) for a portfolio.

    Args:
        portfolio: Optional portfolio dict (uses default if None)
    """
    assembler = PortfolioAssembler()
    d_val = assembler.diversity_score(portfolio) if portfolio else 0.3
    diversity = {"D": d_val}

    if d_val >= 0.5:
        p11_tier = "Tier 1: sufficient diversity"
    elif d_val >= 0.3:
        p11_tier = "Tier 2: marginal — augment portfolio"
    else:
        p11_tier = "Tier 3: insufficient — mandatory augmentation"

    return {
        "diversity": diversity,
        "below_threshold_0_3": d_val < 0.3,
        "p11_tier": p11_tier,
    }


@mcp.tool()
def portfolio_aggregate(
    results: list[dict],
) -> dict:
    """Aggregate concessions across the portfolio.

    Args:
        results: list of concession dicts from portfolio_run
    """
    from absubest.skills.s11_portfolio import PortfolioAssembler

    assembler = PortfolioAssembler()
    # The run() stores concessions; if we reload, use raw results
    concessions = []
    for r in results:
        if isinstance(r, dict):
            concessions.append(r)

    suspicious = [c for c in concessions if c.get("confidence", 1.0) > 0.95]

    return {
        "aggregate_concessions": concessions,
        "n_concessions": len(concessions),
        "suspicious_concessions": len(suspicious),
        "total_results": len(results),
    }


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
