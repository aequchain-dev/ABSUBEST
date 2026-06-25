"""
Stage Executor E — Full-Spectrum Evaluation
"""
from absubest.skills.s7_evaluate import Evaluator


class StageExecutorE:
    mandate = "Full-spectrum evaluation (6 methods, cross-scale coherence)"

    def execute(self, candidates: list[dict], dimensions: list[dict]) -> dict:
        ev = Evaluator()
        scores = ev.evaluate(candidates, dimensions)
        return scores
