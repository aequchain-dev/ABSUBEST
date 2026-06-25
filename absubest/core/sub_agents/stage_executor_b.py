"""
Stage Executor B — Constraint Ontology
"""
from absubest.skills.s4_constraint import ConstraintClassifier


class StageExecutorB:
    mandate = "Constraint classification + liberation"

    def execute(self, analysis_input: dict) -> dict:
        cc = ConstraintClassifier()
        classified = cc.classify(analysis_input)
        liberated = cc.liberation_protocol()
        return {"classified": classified, "liberated": liberated}
