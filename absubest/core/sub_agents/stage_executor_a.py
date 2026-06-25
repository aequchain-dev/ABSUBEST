"""
Stage Executor A — Purpose Crystallization
"""
from absubest.skills.s3_purpose import PurposeCrystallizer


class StageExecutorA:
    mandate = "Purpose crystallization: informal → operational U"

    def execute(self, purpose: str) -> dict:
        pc = PurposeCrystallizer()
        u = pc.crystallize(purpose)
        coh = pc.verify_coherence(u)
        return {"u_spec": u, "coherence": coh}
