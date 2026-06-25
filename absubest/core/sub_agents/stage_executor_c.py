"""
Stage Executor C — Dimension Derivation + Bias
"""
from absubest.skills.s5_dimension import DimensionDeriver


class StageExecutorC:
    mandate = "Dimension derivation + bias disclosure"

    def execute(self, u_spec: dict) -> dict:
        dd = DimensionDeriver()
        dims = dd.derive(u_spec)
        biases = dd.disclose_biases()
        return {"dimensions": dims, "biases": biases}
