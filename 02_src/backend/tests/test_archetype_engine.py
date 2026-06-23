from __future__ import annotations

from app.engines.archetype_engine import ArchetypeEngine
from app.engines.structure_engine import StructureEngine
from app.schemas.naming_input import NamingInput


def test_archetype_engine_uses_only_documented_archetypes(alpha_input) -> None:
    naming_input = NamingInput.from_dict(alpha_input)
    structures = StructureEngine().select(naming_input)["top_structures"]
    result = ArchetypeEngine().select(structures, naming_input)
    allowed = {f"A{index:02d}" for index in range(1, 13)}

    assert result["primary_archetype"]["id"] in allowed
    assert len(result["top_archetypes"]) == 3
    assert all(item["id"] in allowed for item in result["top_archetypes"])
    assert all(item["score_details"] for item in result["top_archetypes"])
