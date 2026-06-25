"""
State Persistence Manager — Checkpoint & resume
"""
from absubest.skills.s14_state import StatePersistence


class StatePersistenceManager:
    mandate = "Checkpoint & resume macro-tasks"

    def checkpoint(self, task_id: str, state: dict, metadata: dict | None = None) -> str:
        sp = StatePersistence()
        return sp.checkpoint(task_id, state, metadata)

    def resume(self, task_id: str) -> dict | None:
        sp = StatePersistence()
        return sp.resume(task_id)
