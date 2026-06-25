"""
Stage Executor F — Optimality Certification
"""
from absubest.skills.s8_certify import Certifier


class StageExecutorF:
    mandate = "Optimality certification with residual risk labeling"

    def execute(self, evaluation: dict, odi: float) -> dict:
        cert = Certifier()
        certificate = cert.certify(evaluation, odi)
        residual = cert.residual_risk_label()
        return {"certificate": certificate, "residual_risk": residual}
