"""
Counter-Optimization Manager — Assemble & run portfolio Π
"""
from absubest.skills.s11_portfolio import PortfolioAssembler


class CounterOptManager:
    mandate = "Assemble & run paradigm-diverse counter-optimizer portfolio"

    def execute(self, purpose: str, best_solution: object) -> dict:
        pa = PortfolioAssembler()
        portfolio = pa.assemble(purpose, best_solution)
        diversity = pa.diversity_score(portfolio)
        concessions = pa.run(portfolio)
        return {"portfolio": portfolio, "diversity": diversity, "concessions": concessions}
