"""
Bias Steward Agent — Bias correction + veto
"""
from absubest.skills.s13_bias import BiasSteward


class BiasStewardAgent:
    mandate = "Bias detection, correction budget, veto"

    def execute(self, task_id: str, scores: dict | None = None) -> dict:
        bs = BiasSteward()
        audit = bs.audit(task_id, scores)
        return {"audit": audit}
