"""
Stage Executor D — Solution-Space Construction
"""
from absubest.skills.s6_coverage import CoverageGenerator


class StageExecutorD:
    mandate = "Solution-space construction with coverage report"

    def execute(self, purpose: str, u_spec: dict, dimensions: list[dict]) -> dict:
        cg = CoverageGenerator()
        candidates = cg.generate(purpose, u_spec, dimensions)
        report = cg.coverage_report()
        return {"candidates": candidates, "report": report}
