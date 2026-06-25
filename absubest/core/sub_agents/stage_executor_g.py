"""
Stage Executor G — Transcendence
"""
from absubest.skills.s9_transcend import Transcender


class StageExecutorG:
    mandate = "Apply transcendence operators to close gaps"

    def execute(
        self, purpose: str, u_spec: dict, evaluation: dict, certificate: dict
    ) -> dict:
        tr = Transcender()
        improved = tr.transcend(purpose, u_spec, evaluation, certificate)
        return {"improved": improved, "gaps": tr._gaps if hasattr(tr, '_gaps') else []}
