"""
Declaration Archivist — Persist declarations + triggers
"""
from absubest.skills.s12_declare import DeclarationDrafter
from absubest.skills.s15_registry import ABSUBESTRegistry


class DeclarationArchivist:
    mandate = "Draft declarations + persist to registry"

    def execute(self, *args, **kwargs) -> dict:
        dd = DeclarationDrafter()
        declaration = dd.draft(*args, **kwargs)

        registry = ABSUBESTRegistry()
        registry_id = registry.archive_adhoc(
            kwargs.get("purpose", ""),
            declaration,
        )
        return {"declaration": declaration, "registry_id": registry_id}
